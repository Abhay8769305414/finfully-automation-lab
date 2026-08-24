import os
import sys
from pathlib import Path

class Config:
    APP_ENV = os.getenv("APP_ENV", "development")
    API_AUTH_TOKEN = os.getenv("API_AUTH_TOKEN", "finfully-stage5a-secret-token")
    DATABASE_BACKEND = os.getenv("DATABASE_BACKEND", "postgres")
    
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB = os.getenv("POSTGRES_DB", "finfully")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_MIN_CONN = int(os.getenv("POSTGRES_MIN_CONN", "1"))
    POSTGRES_MAX_CONN = int(os.getenv("POSTGRES_MAX_CONN", "10"))
    
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")
    CELERY_TASK_ALWAYS_EAGER = os.getenv("CELERY_TASK_ALWAYS_EAGER", "false").lower() == "true"
    
    CUSTOMER_API_URL = os.getenv("CUSTOMER_API_URL", "http://customer-api:8001")
    PRODUCT_API_URL = os.getenv("PRODUCT_API_URL", "http://product-api:8002")
    TAX_API_URL = os.getenv("TAX_API_URL", "http://tax-api:8003")
    ACCOUNTING_API_URL = os.getenv("ACCOUNTING_API_URL", "http://accounting-api:8004")
    NOTIFICATION_API_URL = os.getenv("NOTIFICATION_API_URL", "http://notification-api:8005")
    
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")
    LLM_API_KEY = os.getenv("LLM_API_KEY", "")
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash")

    @classmethod
    def get_database_url(cls) -> str:
        return os.getenv(
            "DATABASE_URL",
            f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}"
        )
