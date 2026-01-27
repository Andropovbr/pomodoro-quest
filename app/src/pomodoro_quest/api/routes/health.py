from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from pomodoro_quest.db.session import get_db_session

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
def liveness() -> dict:
    """
    Liveness probe.

    Indicates whether the application process is running.
    This endpoint must NOT depend on external services.
    """
    return {"status": "alive"}


@router.get("/ready")
def readiness(db: Session = Depends(get_db_session)) -> dict:
    """
    Readiness probe.

    Indicates whether the application is ready to receive traffic.
    This checks critical dependencies such as the database.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        return {"status": "not_ready"}
