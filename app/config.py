import os

from dotenv import load_dotenv


class Settings:
    """Application settings."""
    load_dotenv()

    # Database settings
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_HOST: str = os.getenv("DB_HOST")

    @property
    def database_url(self):
        return (
            f"postgresql://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
