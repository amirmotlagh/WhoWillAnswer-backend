import os
from pydantic_settings import BaseSettings
import sys

# Determine env file path dynamically
ENV = os.getenv('ENV', 'development')
ENV_FILE = f'.env.{ENV}'

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
	REDIS_URL: str = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

	####Database######
	DATABASE_USERNAME: str = 'username'
	DATABASE_PASSWORD: str = 'password'
	DATABASE_HOST: str = 'localhost'
	DATABASE_PORT: int = 5432
	DATABASE_NAME: str = 'wwa_db'
	DATABASE_DBAPI: str = 'postgresql+asyncpg'

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# Override DATABASE_URL with the computed property
		if not self.DEBUG and (
			self.DATABASE_USERNAME == 'username' or self.DATABASE_PASSWORD == 'password'
		):
			raise ValueError('DATABASE_USERNAME and DATABASE_PASSWORD must be set in production')

	@property
	def DATABASE_URL(self) -> str:
		return (
			f'{self.DATABASE_DBAPI}://{self.DATABASE_USERNAME}:'
			f'{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:'
			f'{self.DATABASE_PORT}/{self.DATABASE_NAME}'
		)

	# Default is AsyncAdaptedQueuePool for connection pooling. Override via env var if another strategy is needed.
	DB_POOL_CLASS: str = 'AsyncAdaptedQueuePool'
	DB_POOL_SIZE: int = 10
	DB_MAX_OVERFLOW: int = 20
	DB_POOL_TIMEOUT: int = 30

	MAX_MIGRATION_RETRIES: int = 5
	MIGRATION_INITIAL_DELAY: int = 3
	MIGRATION_MAX_DELAY: int = 30
	MIGRATE: bool = True
	DB_READY_TIMEOUT: int = 60

	# NATS
	NATS_URL: str = 'nats://nats:4222'
	NATS_TOKEN: str | None = None

	model_config = {'env_file': ENV_FILE}


settings = Settings()
