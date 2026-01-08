from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # points to app/

class Settings(BaseSettings):
    env: str = "development"
    open_ai_key: str = "123"
    open_ai_model_name: str = "gpt-4o-mini"
    app_name: str = "VishAgent API"
    host: str = "0.0.0.0"
    port: int = 825

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    log_level: str = "INFO"

    class Config:
        env_file = str(BASE_DIR / ".env.dev")

settings = Settings()
