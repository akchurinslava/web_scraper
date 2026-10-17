from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    ENV_NAME: str
    IS_LOCAL_ENVIRONMENT: bool
    CORS_ORIGINS: list[str]

    # Database settings
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str

    # Docs settings
    DOCS_USERNAME: str
    DOCS_PASSWORD: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    # Redis Queue
    RQ_REDIS_HOST: str
    RQ_REDIS_PORT: int
    RQ_REDIS_PASSWORD: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_EXP_MIN: int
    JWT_REFRESH_EXP_DAYS: int

    @property
    def database_url(self):
        return (
            f"mysql+asyncmy://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading setting for {settings.ENV_NAME} environment.")
    return settings
