from app.config import settings
from app.logger import get_logger
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool, StaticPool, AsyncAdaptedQueuePool

logger = get_logger("app.database.base")

def get_pool_class(pool_class_name: str):
    if pool_class_name == "NullPool":
        return NullPool
    if pool_class_name == "StaticPool":
        return StaticPool
    if pool_class_name == "AsyncAdaptedQueuePool":
        return AsyncAdaptedQueuePool
    raise ValueError(f"Unsupported pool class: {pool_class_name}")

# Load environment variables
DATABASE_URL = settings.DATABASE_URL
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Create async engine with connection pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    poolclass=get_pool_class(settings.DB_POOL_CLASS),
    # Performance optimizations
    # pool_pre_ping=True,  # Validate connections
    # pool_reset_on_return="commit",  # Reset connections

    # Connection arguments
    # connect_args={
        # "server_settings": {
            # "application_name": settings.app_name,
            # "jit": "off",  # Disable JIT for better connection times
        # }
    # }
)

# Database base class
Base = declarative_base()