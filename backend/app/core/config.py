from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    dashboard_origin: str = "http://localhost:8000"
    api_key_pepper: str
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
