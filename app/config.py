import os
from pydantic_settings import BaseSettings
import sys

# Determine env file path dynamically
ENV = os.getenv('ENV', 'development')
ENV_FILE = f".env.{ENV}"

# Explicitly check if the env file exists
if not os.path.exists(ENV_FILE):
    print(f"Warning: Environment file '{ENV_FILE}' does not exist.", file=sys.stderr)


class Settings(BaseSettings):
    ####Redis######
    DEBUG: bool = False
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_MAX_CONNECTIONS: int = 10
    REDIS_PASSWORD: str | None = None
    REDIS_DB: int = 0
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

    ####Database######
    DATABASE_USERNAME: str = os.getenv("DATABASE_USERNAME", "username")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "password")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "5432"))
    DATABASE_NAME: str = os.getenv("POSTGRES_DB", "wwa_db")
    DATABASE_DBAPI: str = os.getenv("DATABASE_DBAPI", "postgresql+asyncpg")
    DATABASE_URL: str = f"{DATABASE_DBAPI}://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    DB_POOL_CLASS: str = os.getenv("DATABASE_POOL_CLASS", "NullPool")
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    DB_POOL_TIMEOUT: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))



    model_config = {
        "env_file": ENV_FILE
    }

settings = Settings()
