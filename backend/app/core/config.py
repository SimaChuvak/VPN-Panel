from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent.parent.parent / ".env"),
        extra="ignore"
    )

    app_env: str = "development"
    database_url: str
    jwt_secret: str
    admin_username: str | None = None
    admin_password: str | None = None
    hostagent_url: str
    hostagent_token: str
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:8080"]


settings = Settings()
