from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from pomodoro_quest.db.session import get_db_session

router = APIRouter()


@router.get("/health", tags=["health"])
def health_check(db: Session = Depends(get_db_session)) -> dict:
    """
    Health endpoint for ALB target group checks.

    This is intentionally lightweight:
    - If the database is reachable, return status=ok.
    - If the database is not reachable, return status=degraded (do not crash).
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception:
        # Avoid leaking internal errors here; logs can capture details later.
        return {"status": "degraded", "db": "unavailable"}
