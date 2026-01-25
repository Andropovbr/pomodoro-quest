from datetime import datetime, timezone
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from pomodoro_quest.db.models import PomodoroSession, SessionMode, SessionStatus
from pomodoro_quest.db.session import get_db_session
from pomodoro_quest.services.xp import calculate_xp

from pomodoro_quest.services.demo_user import get_or_create_demo_user
from pomodoro_quest.db.models import User


router = APIRouter(prefix="/sessions", tags=["sessions"])


class StartSessionRequest(BaseModel):
    mode: SessionMode
    planned_minutes: int = Field(ge=1, le=240)


class StartSessionResponse(BaseModel):
    session_id: str
    status: SessionStatus
    started_at: datetime


class CompleteSessionRequest(BaseModel):
    session_id: str
    completed_minutes: int = Field(ge=1, le=240)


class CompleteSessionResponse(BaseModel):
    session_id: str
    status: SessionStatus
    completed_at: datetime
    xp_gained: int


@router.post("/start", response_model=StartSessionResponse)
def start_session(payload: StartSessionRequest, db: Session = Depends(get_db_session)) -> StartSessionResponse:
    user = get_or_create_demo_user(db)

    session = PomodoroSession(
        user_id=user.id,
        mode=payload.mode,
        planned_minutes=payload.planned_minutes,
        status=SessionStatus.running,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return StartSessionResponse(
        session_id=session.id,
        status=session.status,
        started_at=session.started_at,
    )



@router.post("/complete", response_model=CompleteSessionResponse)
def complete_session(payload: CompleteSessionRequest, db: Session = Depends(get_db_session)) -> CompleteSessionResponse:
    session: PomodoroSession | None = db.get(PomodoroSession, payload.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status != SessionStatus.running:
        raise HTTPException(status_code=409, detail="Session is not running")

    session.completed_minutes = payload.completed_minutes
    session.status = SessionStatus.completed
    session.completed_at = datetime.now(timezone.utc)

    xp_gained = calculate_xp(session.mode)

    user: User | None = db.get(User, session.user_id)
    if user is None:
        # This should not happen. If it does, we have data integrity issues.
        raise HTTPException(status_code=500, detail="Session owner user not found")

    user.xp += xp_gained
    user.level = (user.xp // 100) + 1  # level 1: 0-99, level 2: 100-199, etc.

    db.add(session)
    db.add(user)
    db.commit()
    db.refresh(session)

    return CompleteSessionResponse(
        session_id=session.id,
        status=session.status,
        completed_at=session.completed_at,
        xp_gained=xp_gained,
    )

