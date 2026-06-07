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
    DATABASE_USERNAME: str = "username"
    DATABASE_PASSWORD: str = "password"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "wwa_db"
    DATABASE_DBAPI: str = "postgresql+asyncpg"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"{self.DATABASE_DBAPI}://{self.DATABASE_USERNAME}:"
            f"{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    DB_POOL_CLASS: str = "NullPool"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30

    MAX_MIGRATION_RETRIES: int = 5
    INITIAL_DELAY: int = 3
    MAX_DELAY: int = 20
    MIGRATE: bool = False

    #NATS
    NATS_URL: str = "nats://nats:4222"
    NATS_TOKEN: str | None = None

    model_config = {
        "env_file": ENV_FILE
    }

settings = Settings()
