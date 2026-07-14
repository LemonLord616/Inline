import asyncio
import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from database import async_session
from models import Queue, Participant, SwapRequest, QueueStatus, ParticipantStatus, LatecomerPolicy

logger = logging.getLogger("inline.tasks")

SWAP_TIMEOUT_MINUTES = 10


async def background_loop():
    while True:
        try:
            async with async_session() as db:
                now = datetime.now(timezone.utc)

                queues_result = await db.execute(
                    select(Queue).where(Queue.status != QueueStatus.CLOSED)
                )
                queues = queues_result.scalars().all()

                for queue in queues:
                    window = queue.safe_window_minutes or 5
                    if window > 0:
                        called_result = await db.execute(
                            select(Participant).where(
                                Participant.queue_id == queue.id,
                                Participant.status == ParticipantStatus.CALLED,
                                Participant.called_at.isnot(None),
                            )
                        )
                        for p in called_result.scalars().all():
                            elapsed = (now - p.called_at).total_seconds() / 60
                            if elapsed < window:
                                continue
                            if queue.latecomer_policy == LatecomerPolicy.DISCARD:
                                p.status = ParticipantStatus.SKIPPED
                                p.called_at = None
                                logger.info(f"Discarded latecomer {p.name} in queue {queue.id}")
                            else:
                                max_pos_r = await db.execute(
                                    select(Participant.position).where(
                                        Participant.queue_id == queue.id,
                                        Participant.status.in_([
                                            ParticipantStatus.WAITING,
                                            ParticipantStatus.CALLED,
                                            ParticipantStatus.DELAYED,
                                        ]),
                                    ).order_by(Participant.position.desc()).limit(1)
                                )
                                p.status = ParticipantStatus.WAITING
                                p.called_at = None
                                p.position = (max_pos_r.scalar() or 0) + 1
                                logger.info(f"Moved latecomer {p.name} to end in queue {queue.id}")

                    swap_cutoff = now - timedelta(minutes=SWAP_TIMEOUT_MINUTES)
                    stale_result = await db.execute(
                        select(SwapRequest).where(
                            SwapRequest.queue_id == queue.id,
                            SwapRequest.status == "pending",
                            SwapRequest.created_at < swap_cutoff,
                        )
                    )
                    for s in stale_result.scalars().all():
                        s.status = "expired"
                        logger.info(f"Expired swap {s.id} in queue {queue.id}")

                await db.commit()
        except Exception as e:
            logger.error(f"Background loop failed: {e}")

        await asyncio.sleep(15)
