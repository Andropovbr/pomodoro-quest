from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
def health_check() -> dict:
    """
    Health endpoint for ALB target group checks.
    """
    return {"status": "ok"}
