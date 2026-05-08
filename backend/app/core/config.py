from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "小红贸 API"
    app_version: str = "0.1.0"
    debug: bool = True
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    database_url: str = "postgresql+asyncpg://xiaohongmao:xiaohongmao_dev@localhost:5432/xiaohongmao"
    redis_url: str = "redis://localhost:6379/0"
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "xiaohongmao"
    minio_secret_key: str = "xiaohongmao_dev_password"


settings = Settings()
