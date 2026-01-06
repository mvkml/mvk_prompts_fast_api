from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "development"
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
        env_file = ".env.dev"

settings = Settings()
