from contextlib import asynccontextmanager

from fastapi import FastAPI

from pomodoro_quest.core.config import settings
from pomodoro_quest.core.logging import configure_logging
from pomodoro_quest.db.base import Base
from pomodoro_quest.db.session import engine
from pomodoro_quest.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    Startup:
    - Ensure database schema is created before serving requests.

    Shutdown:
    - No-op for now.
    """
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (nothing yet)


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
    )

    app.include_router(api_router)
    return app


app = create_app()
