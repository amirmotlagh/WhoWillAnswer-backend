import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = False
    class Config:
        env_file = f".env.{os.getenv('ENV', 'development')}"
settings = Settings()
