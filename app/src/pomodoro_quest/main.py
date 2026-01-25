from fastapi import FastAPI

from pomodoro_quest.core.config import settings
from pomodoro_quest.core.logging import configure_logging
from pomodoro_quest.db.base import Base
from pomodoro_quest.db.session import engine
from pomodoro_quest.api import api_router


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(title=settings.app_name)

    @app.on_event("startup")
    def on_startup() -> None:
        # Phase 0: auto-create tables on startup.
        # We'll replace this with Alembic migrations later.
        Base.metadata.create_all(bind=engine)

    app.include_router(api_router)
    return app


app = create_app()
