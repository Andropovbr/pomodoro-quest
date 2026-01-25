from fastapi import APIRouter

from pomodoro_quest.api.routes.health import router as health_router
from pomodoro_quest.api.routes.sessions import router as sessions_router
from pomodoro_quest.api.routes.stats import router as stats_router
from pomodoro_quest.api.routes.me import router as me_router

api_router = APIRouter(prefix="/api")
api_router.include_router(health_router)
api_router.include_router(sessions_router)
api_router.include_router(stats_router)
api_router.include_router(me_router)
