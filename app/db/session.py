from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings

settings = get_settings()

# Use your actual DB connection string
DATABASE_URL = settings.database_url

engine: AsyncEngine = create_async_engine(
    DATABASE_URL, echo=False, future=True  # flip to True for debugging SQL output
)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
