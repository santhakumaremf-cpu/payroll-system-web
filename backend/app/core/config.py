from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Payroll System"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "payroll-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 hours

    class Config:
        case_sensitive = True


settings = Settings()
