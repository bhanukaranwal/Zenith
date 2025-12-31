from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    DATABASE_URL: str = "postgresql+asyncpg://zenith:zenith_pass@localhost:5432/zenith"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    S3_ENDPOINT: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    S3_BUCKET: str = "zenith-artifacts"
    
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    OTEL_ENABLED: bool = True
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4318"
    OTEL_SERVICE_NAME: str = "zenith-backend"
    
    TRITON_URL: str = "http://localhost:8001"
    
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    MAX_UPLOAD_SIZE: int = 1024 * 1024 * 1024
    
    FEATURE_STORE_ONLINE_TTL: int = 86400
    
    DRIFT_THRESHOLD: float = 0.05
    DRIFT_CHECK_INTERVAL: int = 3600


settings = Settings()
