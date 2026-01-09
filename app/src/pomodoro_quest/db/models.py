import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Integer, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from pomodoro_quest.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SessionMode(str, enum.Enum):
    focus = "focus"
    break_short = "break_short"
    break_long = "break_long"


class SessionStatus(str, enum.Enum):
    running = "running"
    completed = "completed"
    canceled = "canceled"


class PomodoroSession(Base):
    """
    A single pomodoro-like session.

    Phase 0 simplification:
    - No authentication/user yet. We'll add user_id after Cognito.
    """

    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mode: Mapped[SessionMode] = mapped_column(Enum(SessionMode), nullable=False)

    planned_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    status: Mapped[SessionStatus] = mapped_column(Enum(SessionStatus), nullable=False, default=SessionStatus.running)

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
