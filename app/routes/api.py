from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import get_db
from models import Queue, Participant, SwapRequest, QueueStatus, ParticipantStatus, LatecomerPolicy
from models.models import gen_4digit_code
import secrets
from datetime import datetime, timezone, timedelta

router = APIRouter(prefix="/api")


def calc_slot(start_time_str: str, slot_dur_min: int, group_idx: int):
    try:
        h, m = map(int, start_time_str.split(":"))
    except Exception:
        h, m = 9, 0
    base = datetime(2026, 1, 1, h, m)
    slot_start = base + timedelta(minutes=slot_dur_min * group_idx)
    slot_end = slot_start + timedelta(minutes=slot_dur_min)
    return slot_start.strftime("%H:%M"), slot_end.strftime("%H:%M")


async def get_slot_counts(db: AsyncSession, queue_id: str):
    result = await db.execute(
        select(Participant.slot_group, func.count()).where(
            Participant.queue_id == queue_id,
            Participant.status.in_([ParticipantStatus.WAITING, ParticipantStatus.CALLED, ParticipantStatus.DELAYED]),
            Participant.slot_group.isnot(None),
        ).group_by(Participant.slot_group)
    )
    return dict(result.all())


async def find_next_slot(db: AsyncSession, queue_id: str, max_per_slot: int):
    counts = await get_slot_counts(db, queue_id)
    for i in range(max_per_slot * 200):
        if counts.get(i, 0) < max_per_slot:
            return i
    return 0


@router.post("/queue/create")
async def create_queue(
    name: str = Form(...),
    description: str = Form(""),
    max_size: int = Form(50),
    max_per_slot: int = Form(1),
    allow_swap: bool = Form(False),
    allow_delay: bool = Form(True),
    safe_window_minutes: int = Form(5),
    latecomer_policy: str = Form("to_end"),
    slot_duration_minutes: int = Form(30),
    start_time: str = Form("09:00"),
    info: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    token = secrets.token_urlsafe(16)
    code = gen_4digit_code()
    while True:
        existing = await db.execute(select(Queue).where(Queue.code == code))
        if not existing.scalar_one_or_none():
            break
        code = gen_4digit_code()

    queue = Queue(
        code=code,
        name=name,
        description=description,
        organizer_token=token,
        max_size=max_size,
        max_per_slot=max(max_per_slot, 1),
        allow_swap=allow_swap,
        allow_delay=allow_delay,
        safe_window_minutes=safe_window_minutes,
        latecomer_policy=LatecomerPolicy(latecomer_policy),
        slot_duration_minutes=slot_duration_minutes,
        start_time=start_time,
        info=info if info.strip() else None,
    )
    db.add(queue)
    await db.commit()
    await db.refresh(queue)
    return {"queue_id": queue.id, "queue_code": queue.code, "organizer_token": token}


@router.get("/queue/{queue_id}")
async def get_queue(queue_id: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue:
        raise HTTPException(404, "Queue not found")
    result = await db.execute(
        select(Participant).where(Participant.queue_id == queue_id).order_by(Participant.position)
    )
    participants = result.scalars().all()

    slot_dur = queue.slot_duration_minutes or 30
    start_t = queue.start_time or "09:00"
    max_per = queue.max_per_slot or 1

    slot_data = []
    for p in participants:
        group = p.slot_group if p.slot_group is not None else 0
        slot_start, slot_end = calc_slot(start_t, slot_dur, group)

        item = {
            "id": p.id,
            "name": p.name,
            "position": p.position,
            "slot_group": group,
            "status": p.status.value,
            "user_token": p.user_token,
            "joined_at": p.joined_at.isoformat(),
            "called_at": p.called_at.isoformat() if p.called_at else None,
            "served_at": p.served_at.isoformat() if p.served_at else None,
            "slot_start": slot_start,
            "slot_end": slot_end,
            "slot_label": None,
        }

        if p.status in (ParticipantStatus.WAITING, ParticipantStatus.DELAYED):
            item["slot_label"] = f"{slot_start} – {slot_end}"
        elif p.status == ParticipantStatus.CALLED:
            item["slot_label"] = "Сейчас"
        elif p.status == ParticipantStatus.SERVED:
            item["slot_label"] = "Обслужён"
        elif p.status == ParticipantStatus.SKIPPED:
            item["slot_label"] = "Пропущен"

        slot_data.append(item)

    swaps_result = await db.execute(
        select(SwapRequest).where(SwapRequest.queue_id == queue_id, SwapRequest.status == "pending")
    )
    pending_swaps = swaps_result.scalars().all()

    slot_counts = await get_slot_counts(db, queue_id)

    slots_info = []
    max_slot = max((slot_counts.keys() or {0})) if slot_counts else 0
    for i in range(max_slot + 1):
        ss, se = calc_slot(start_t, slot_dur, i)
        slots_info.append({
            "index": i,
            "start": ss,
            "end": se,
            "label": f"{ss} – {se}",
            "count": slot_counts.get(i, 0),
            "max": max_per,
        })

    return {
        "id": queue.id,
        "code": queue.code,
        "name": queue.name,
        "description": queue.description,
        "status": queue.status.value,
        "max_size": queue.max_size,
        "max_per_slot": max_per,
        "allow_swap": queue.allow_swap,
        "allow_delay": queue.allow_delay,
        "safe_window_minutes": queue.safe_window_minutes,
        "latecomer_policy": queue.latecomer_policy.value,
        "slot_duration_minutes": slot_dur,
        "start_time": start_t,
        "info": queue.info,
        "created_at": queue.created_at.isoformat(),
        "slots": slots_info,
        "participants": slot_data,
        "participant_count": len(participants),
        "pending_swaps": [
            {
                "id": s.id,
                "from_id": s.from_participant_id,
                "from_name": s.from_participant.name if s.from_participant else "?",
                "swap_type": s.swap_type,
                "target_slot_group": s.target_slot_group,
                "target_slot_label": (
                    f"{calc_slot(start_t, slot_dur, s.target_slot_group)[0]} – {calc_slot(start_t, slot_dur, s.target_slot_group)[1]}"
                    if s.target_slot_group is not None else None
                ),
                "target_position": s.target_position,
            }
            for s in pending_swaps
        ],
    }


@router.get("/queue/by-code/{code}")
async def get_queue_by_code(code: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Queue).where(Queue.code == code))
    queue = result.scalar_one_or_none()
    if not queue:
        raise HTTPException(404, "Queue not found")
    return {"queue_id": queue.id, "code": queue.code, "name": queue.name}


@router.post("/queue/{queue_id}/join")
async def join_queue(
    queue_id: str,
    name: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    queue = await db.get(Queue, queue_id)
    if not queue:
        raise HTTPException(404, "Queue not found")
    if queue.status != QueueStatus.ACTIVE:
        raise HTTPException(400, "Queue is not active")

    count_result = await db.execute(
        select(func.count()).select_from(Participant).where(
            Participant.queue_id == queue_id,
            Participant.status.in_([ParticipantStatus.WAITING, ParticipantStatus.CALLED, ParticipantStatus.DELAYED]),
        )
    )
    current_count = count_result.scalar()
    if current_count >= queue.max_size:
        raise HTTPException(400, "Queue is full")

    pos_result = await db.execute(
        select(func.max(Participant.position)).where(Participant.queue_id == queue_id)
    )
    max_pos = pos_result.scalar() or 0

    slot_group = await find_next_slot(db, queue_id, queue.max_per_slot or 1)

    user_token = secrets.token_urlsafe(16)
    participant = Participant(
        queue_id=queue_id,
        name=name,
        position=max_pos + 1,
        slot_group=slot_group,
        status=ParticipantStatus.WAITING,
        user_token=user_token,
    )
    db.add(participant)
    await db.commit()
    await db.refresh(participant)
    return {"participant_id": participant.id, "user_token": user_token, "position": participant.position, "slot_group": slot_group}


@router.post("/queue/{queue_id}/admin/{token}/next")
async def next_in_queue(queue_id: str, token: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        raise HTTPException(403, "Unauthorized")
    if queue.status != QueueStatus.ACTIVE:
        raise HTTPException(400, "Queue is not active")

    result = await db.execute(
        select(Participant).where(
            Participant.queue_id == queue_id,
            Participant.status.in_([ParticipantStatus.WAITING, ParticipantStatus.DELAYED]),
        ).order_by(Participant.position).limit(1)
    )
    current = result.scalar_one_or_none()
    if current:
        current.status = ParticipantStatus.CALLED
        current.called_at = datetime.now(timezone.utc)
        await db.commit()
        return {"called": {"id": current.id, "name": current.name, "position": current.position}}
    return {"called": None}


@router.post("/queue/{queue_id}/admin/{token}/serve/{participant_id}")
async def serve_participant(queue_id: str, token: str, participant_id: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        raise HTTPException(403, "Unauthorized")
    participant = await db.get(Participant, participant_id)
    if not participant or participant.queue_id != queue_id:
        raise HTTPException(404, "Participant not found")
    participant.status = ParticipantStatus.SERVED
    participant.served_at = datetime.now(timezone.utc)
    await db.commit()
    return {"ok": True}


@router.post("/queue/{queue_id}/admin/{token}/undo/{participant_id}")
async def undo_participant(queue_id: str, token: str, participant_id: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        raise HTTPException(403, "Unauthorized")
    participant = await db.get(Participant, participant_id)
    if not participant or participant.queue_id != queue_id:
        raise HTTPException(404, "Participant not found")
    if participant.status in (ParticipantStatus.SERVED, ParticipantStatus.SKIPPED):
        participant.status = ParticipantStatus.WAITING
        participant.served_at = None
        participant.called_at = None
        await db.commit()
    return {"ok": True}


@router.post("/queue/{queue_id}/admin/{token}/skip/{participant_id}")
async def skip_participant(queue_id: str, token: str, participant_id: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        raise HTTPException(403, "Unauthorized")
    participant = await db.get(Participant, participant_id)
    if not participant or participant.queue_id != queue_id:
        raise HTTPException(404, "Participant not found")
    participant.status = ParticipantStatus.SKIPPED
    await db.commit()
    return {"ok": True}


@router.post("/queue/{queue_id}/admin/{token}/set-slot")
async def set_slot_group(
    queue_id: str, token: str,
    participant_id: str = Form(...),
    slot_group: int = Form(...),
    db: AsyncSession = Depends(get_db),
):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        raise HTTPException(403, "Unauthorized")
    participant = await db.get(Participant, participant_id)
    if not participant or participant.queue_id != queue_id:
        raise HTTPException(404, "Participant not found")
    participant.slot_group = slot_group
    await db.commit()
    return {"ok": True}


@router.post("/queue/{queue_id}/admin/{token}/set-slot-batch")
async def set_slot_batch(
    queue_id: str, token: str,
    participant_ids: str = Form(...),
    slot_group: int = Form(...),
    db: AsyncSession = Depends(get_db),
):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        raise HTTPException(403, "Unauthorized")
    ids = [x.strip() for x in participant_ids.split(",") if x.strip()]
    count = 0
    for pid in ids:
        participant = await db.get(Participant, pid)
        if participant and participant.queue_id == queue_id:
            participant.slot_group = slot_group
            count += 1
    await db.commit()
    return {"ok": True, "updated": count}


@router.post("/queue/{queue_id}/admin/{token}/pause")
async def pause_queue(queue_id: str, token: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        raise HTTPException(403, "Unauthorized")
    queue.status = QueueStatus.PAUSED
    await db.commit()
    return {"status": "paused"}


@router.post("/queue/{queue_id}/admin/{token}/resume")
async def resume_queue(queue_id: str, token: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        raise HTTPException(403, "Unauthorized")
    queue.status = QueueStatus.ACTIVE
    await db.commit()
    return {"status": "active"}


@router.post("/queue/{queue_id}/admin/{token}/reopen")
async def reopen_queue(queue_id: str, token: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        raise HTTPException(403, "Unauthorized")
    if queue.status != QueueStatus.CLOSED:
        raise HTTPException(400, "Queue is not closed")
    queue.status = QueueStatus.ACTIVE
    await db.commit()
    return {"status": "active"}


@router.post("/queue/{queue_id}/admin/{token}/close")
async def close_queue(queue_id: str, token: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        raise HTTPException(403, "Unauthorized")
    queue.status = QueueStatus.CLOSED
    await db.commit()
    return {"status": "closed"}


@router.post("/queue/{queue_id}/admin/{token}/update-settings")
async def update_settings(
    queue_id: str, token: str,
    allow_swap: bool = Form(False),
    allow_delay: bool = Form(True),
    safe_window_minutes: int = Form(5),
    latecomer_policy: str = Form("to_end"),
    slot_duration_minutes: int = Form(30),
    start_time: str = Form("09:00"),
    max_per_slot: int = Form(1),
    info: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        raise HTTPException(403, "Unauthorized")
    queue.allow_swap = allow_swap
    queue.allow_delay = allow_delay
    queue.safe_window_minutes = safe_window_minutes
    queue.latecomer_policy = LatecomerPolicy(latecomer_policy)
    queue.slot_duration_minutes = slot_duration_minutes
    queue.start_time = start_time
    queue.max_per_slot = max(max_per_slot, 1)
    queue.info = info if info.strip() else None
    await db.commit()
    return {"ok": True}


@router.post("/queue/{queue_id}/delay/{participant_id}")
async def mark_delayed(queue_id: str, participant_id: str, user_token: str = Form(...), db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue:
        raise HTTPException(404, "Queue not found")
    if queue.status != QueueStatus.ACTIVE:
        raise HTTPException(400, "Queue is not active")
    if not queue.allow_delay:
        raise HTTPException(400, "Delay is not allowed")
    participant = await db.get(Participant, participant_id)
    if not participant or participant.queue_id != queue_id or participant.user_token != user_token:
        raise HTTPException(403, "Unauthorized")
    participant.status = ParticipantStatus.DELAYED
    await db.commit()
    return {"ok": True}


@router.post("/queue/{queue_id}/swap/request")
async def request_swap(
    queue_id: str,
    from_id: str = Form(...),
    from_token: str = Form(...),
    swap_type: str = Form("slot_change"),
    target_slot_group: int = Form(None),
    target_position: int = Form(None),
    db: AsyncSession = Depends(get_db),
):
    queue = await db.get(Queue, queue_id)
    if not queue:
        raise HTTPException(404, "Queue not found")
    if queue.status != QueueStatus.ACTIVE:
        raise HTTPException(400, "Queue is not active")
    if not queue.allow_swap:
        raise HTTPException(400, "Swap is not allowed")
    from_p = await db.get(Participant, from_id)
    if not from_p or from_p.user_token != from_token:
        raise HTTPException(403, "Unauthorized")

    existing = await db.execute(
        select(SwapRequest).where(
            SwapRequest.queue_id == queue_id,
            SwapRequest.from_participant_id == from_id,
            SwapRequest.status == "pending",
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(400, "You already have a pending request")

    swap = SwapRequest(
        queue_id=queue_id,
        from_participant_id=from_id,
        swap_type=swap_type,
        target_slot_group=target_slot_group,
        target_position=target_position,
        status="pending",
    )
    db.add(swap)
    await db.commit()
    await db.refresh(swap)
    return {"swap_id": swap.id}


@router.post("/queue/{queue_id}/swap/cancel/{swap_id}")
async def cancel_swap(queue_id: str, swap_id: str, user_token: str = Form(...), db: AsyncSession = Depends(get_db)):
    swap = await db.get(SwapRequest, swap_id)
    if not swap or swap.queue_id != queue_id:
        raise HTTPException(404, "Swap not found")
    from_p = await db.get(Participant, swap.from_participant_id)
    if not from_p or from_p.user_token != user_token:
        raise HTTPException(403, "Unauthorized")
    swap.status = "cancelled"
    await db.commit()
    return {"ok": True}


@router.post("/queue/{queue_id}/admin/{token}/swap/{swap_id}/accept")
async def accept_swap(queue_id: str, token: str, swap_id: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        raise HTTPException(403, "Unauthorized")
    swap = await db.get(SwapRequest, swap_id)
    if not swap or swap.queue_id != queue_id or swap.status != "pending":
        raise HTTPException(404, "Swap not found or already processed")

    from_p = await db.get(Participant, swap.from_participant_id)
    if not from_p:
        raise HTTPException(404, "Participant not found")

    if swap.swap_type == "slot_change" and swap.target_slot_group is not None:
        from_p.slot_group = swap.target_slot_group
    elif swap.swap_type == "position_change":
        if swap.to_participant_id:
            to_p = await db.get(Participant, swap.to_participant_id)
            if to_p:
                from_p.position, to_p.position = to_p.position, from_p.position
        elif swap.target_position is not None:
            slotmates = await db.execute(
                select(Participant).where(
                    Participant.queue_id == queue_id,
                    Participant.slot_group == from_p.slot_group,
                    Participant.status.in_([ParticipantStatus.WAITING, ParticipantStatus.CALLED, ParticipantStatus.DELAYED]),
                ).order_by(Participant.position)
            )
            peers = list(slotmates.scalars().all())
            peers = [p for p in peers if p.id != from_p.id]
            if swap.target_position == 0 and peers:
                from_p.position = min(p.position for p in peers) - 1
            elif peers:
                from_p.position = max(p.position for p in peers) + 1
            else:
                from_p.position = from_p.position

    swap.status = "accepted"

    pos_result = await db.execute(
        select(Participant).where(
            Participant.queue_id == queue_id,
            Participant.status.in_([ParticipantStatus.WAITING, ParticipantStatus.CALLED, ParticipantStatus.DELAYED]),
        ).order_by(Participant.position)
    )
    active = list(pos_result.scalars().all())
    for i, p in enumerate(active):
        p.position = i + 1

    await db.commit()
    return {"ok": True}


@router.post("/queue/{queue_id}/admin/{token}/swap/{swap_id}/reject")
async def reject_swap(queue_id: str, token: str, swap_id: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        raise HTTPException(403, "Unauthorized")
    swap = await db.get(SwapRequest, swap_id)
    if not swap or swap.queue_id != queue_id:
        raise HTTPException(404, "Swap not found")
    swap.status = "rejected"
    await db.commit()
    return {"ok": True}
