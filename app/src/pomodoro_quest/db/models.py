import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Integer, DateTime, Enum
from sqlalchemy import ForeignKey
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


class User(Base):
    """
    Demo user for Phase 0.

    Once we add Cognito, we'll replace this with a stable user_id from JWT claims.
    """

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    xp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)



class PomodoroSession(Base):
    """
    A single pomodoro-like session.
    """

    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        nullable=False,
    )

    mode: Mapped[SessionMode] = mapped_column(Enum(SessionMode), nullable=False)

    planned_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus),
        nullable=False,
        default=SessionStatus.running,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

