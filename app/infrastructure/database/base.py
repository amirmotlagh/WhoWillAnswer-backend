from app.config import settings
from app.logger import get_logger
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool, StaticPool, AsyncAdaptedQueuePool

logger = get_logger('app.database.base')


def get_pool_class(pool_class_name: str):
	if pool_class_name == 'NullPool':
		return NullPool
	if pool_class_name == 'StaticPool':
		return StaticPool
	if pool_class_name == 'AsyncAdaptedQueuePool':
		return AsyncAdaptedQueuePool
	raise ValueError(f'Unsupported pool class: {pool_class_name}')


# Load environment variables
DATABASE_URL = settings.DATABASE_URL
if not DATABASE_URL:
	raise ValueError('DATABASE_URL environment variable is required')

pool_class = get_pool_class(settings.DB_POOL_CLASS)
engine_kwargs = {'echo': settings.DEBUG, 'poolclass': pool_class}
if pool_class is AsyncAdaptedQueuePool:
	engine_kwargs.update(
		pool_size=settings.DB_POOL_SIZE,
		max_overflow=settings.DB_MAX_OVERFLOW,
		pool_timeout=settings.DB_POOL_TIMEOUT,
	)
# Create async engine with connection pooling
engine = create_async_engine(
	DATABASE_URL,
	**engine_kwargs,
	# Performance optimizations
	pool_pre_ping=True,  # Validate connections
	pool_reset_on_return='rollback',  # Reset connections safely
	# Connection arguments
	connect_args={
		'server_settings': {
			'application_name': 'WhoWillAnswer',
			'jit': 'off',  # Disable JIT for better connection times
		}
	},
)

# Database base class
Base = declarative_base()
