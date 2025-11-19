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
    DEBUG: bool = False
    model_config = {
        "env_file": ENV_FILE
    }

settings = Settings()
