from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL : str # Database

    #jwt
    SECRET_KEY : str
    ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : int

    APP_NAME: str = "To-Do List API"
    VERSION: str= "1.0.0"

    class Config:
        env_file = ".env"

settings = Settings()
