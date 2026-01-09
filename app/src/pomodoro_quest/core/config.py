from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    app_name: str = "pomodoro-quest"
    environment: str = "dev"
    log_level: str = "INFO"

    # Store SQLite DB under the user's home directory to avoid filesystem quirks
    # (e.g., VirtualBox shared folders like vboxsf).
    database_url: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url

        data_dir = Path.home() / ".local" / "share" / "pomodoro-quest"
        data_dir.mkdir(parents=True, exist_ok=True)
        db_path = data_dir / "app.db"
        return f"sqlite:///{db_path}"


settings = Settings()
