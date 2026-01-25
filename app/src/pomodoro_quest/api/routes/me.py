from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from pomodoro_quest.db.session import get_db_session
from pomodoro_quest.services.demo_user import get_or_create_demo_user


router = APIRouter(tags=["me"])


class MeResponse(BaseModel):
    username: str
    xp: int
    level: int


@router.get("/me", response_model=MeResponse)
def me(db: Session = Depends(get_db_session)) -> MeResponse:
    user = get_or_create_demo_user(db)
    return MeResponse(username=user.username, xp=user.xp, level=user.level)
