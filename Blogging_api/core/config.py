from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REDIS_URL: str

    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    APP_NAME: str = "THE BLOG API"
    VERSION: str = "1.0.0"


    model_config = SettingsConfigDict(env_file= Path(__file__).resolve().parent.parent / ".env")

settings = Settings()