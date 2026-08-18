from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str 

    GEMINI_API_KEY:str
    
    APP_NAME: str = "RECIPE API"
    VERSION: str = "1.0.0"

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parent.parent / ".env")


settings = Settings()
