from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from pomodoro_quest.db.models import PomodoroSession, SessionMode, SessionStatus
from pomodoro_quest.db.session import get_db_session
from pomodoro_quest.services.demo_user import get_or_create_demo_user


router = APIRouter(prefix="/stats", tags=["stats"])


class TodayStatsResponse(BaseModel):
    focus_sessions_completed: int
    break_sessions_completed: int
    total_completed_minutes: int


@router.get("/today", response_model=TodayStatsResponse)
def today_stats(db: Session = Depends(get_db_session)) -> TodayStatsResponse:
    user = get_or_create_demo_user(db)

    now = datetime.now(timezone.utc)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    sessions = (
        db.query(PomodoroSession)
        .filter(PomodoroSession.user_id == user.id)
        .filter(PomodoroSession.status == SessionStatus.completed)
        .filter(PomodoroSession.completed_at >= start_of_day)
        .filter(PomodoroSession.completed_at < end_of_day)
        .all()
    )

    focus_count = sum(1 for s in sessions if s.mode == SessionMode.focus)
    break_count = sum(1 for s in sessions if s.mode in (SessionMode.break_short, SessionMode.break_long))
    total_minutes = sum((s.completed_minutes or 0) for s in sessions)

    return TodayStatsResponse(
        focus_sessions_completed=focus_count,
        break_sessions_completed=break_count,
        total_completed_minutes=total_minutes,
    )
