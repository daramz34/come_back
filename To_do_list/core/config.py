from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path



class Settings(BaseSettings):
    DATABASE_URL : str # Database

    #jwt
    SECRET_KEY : str
    ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : int

    APP_NAME: str = "To-Do List API"
    VERSION: str= "1.0.0"


    model_config = SettingsConfigDict(env_file= Path(__file__).resolve().parent.parent / ".env")


settings = Settings()