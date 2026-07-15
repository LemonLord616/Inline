from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
import uuid
import random

from database import Base


def gen_id():
    return uuid.uuid4().hex[:12]


def gen_4digit_code():
    return str(random.randint(1000, 9999))


class QueueStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"


class ParticipantStatus(str, enum.Enum):
    WAITING = "waiting"
    CALLED = "called"
    SERVED = "served"
    DELAYED = "delayed"
    SKIPPED = "skipped"


class LatecomerPolicy(str, enum.Enum):
    TO_END = "to_end"
    DISCARD = "discard"


class Queue(Base):
    __tablename__ = "queues"

    id = Column(String, primary_key=True, default=gen_id)
    code = Column(String(4), nullable=False, unique=True, default=gen_4digit_code)
    name = Column(String(100), nullable=False)
    description = Column(Text, default="")
    organizer_token = Column(String, nullable=False, unique=True)
    status = Column(SAEnum(QueueStatus), default=QueueStatus.ACTIVE)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    max_size = Column(Integer, default=50)
    allow_swap = Column(Boolean, default=False)
    allow_delay = Column(Boolean, default=True)
    safe_window_minutes = Column(Integer, default=5)
    latecomer_policy = Column(SAEnum(LatecomerPolicy), default=LatecomerPolicy.TO_END)
    is_premium = Column(Boolean, default=False)

    use_time_slots = Column(Boolean, default=True)
    slot_duration_minutes = Column(Integer, default=30)
    start_time = Column(String(5), default="09:00")
    max_per_slot = Column(Integer, default=1)
    info = Column(Text, nullable=True)

    participants = relationship("Participant", back_populates="queue", cascade="all, delete-orphan")
    swap_requests = relationship("SwapRequest", back_populates="queue", cascade="all, delete-orphan")


class Participant(Base):
    __tablename__ = "participants"

    id = Column(String, primary_key=True, default=gen_id)
    queue_id = Column(String, ForeignKey("queues.id"), nullable=False)
    name = Column(String(100), nullable=False)
    position = Column(Integer, nullable=False)
    slot_group = Column(Integer, nullable=True)
    status = Column(SAEnum(ParticipantStatus), default=ParticipantStatus.WAITING)
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    called_at = Column(DateTime, nullable=True)
    served_at = Column(DateTime, nullable=True)
    user_token = Column(String, nullable=False)

    queue = relationship("Queue", back_populates="participants")


class SwapRequest(Base):
    __tablename__ = "swap_requests"

    id = Column(String, primary_key=True, default=gen_id)
    queue_id = Column(String, ForeignKey("queues.id"), nullable=False)
    from_participant_id = Column(String, ForeignKey("participants.id"), nullable=False)
    to_participant_id = Column(String, ForeignKey("participants.id"), nullable=True)
    swap_type = Column(String(20), default="slot_change")
    target_slot_group = Column(Integer, nullable=True)
    target_position = Column(Integer, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    queue = relationship("Queue", back_populates="swap_requests")
    from_participant = relationship("Participant", foreign_keys=[from_participant_id])
    to_participant = relationship("Participant", foreign_keys=[to_participant_id])
