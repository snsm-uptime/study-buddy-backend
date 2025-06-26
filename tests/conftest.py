import os
from collections.abc import AsyncGenerator, Generator
from typing import AsyncIterator
from unittest.mock import AsyncMock

from app.dependencies.file import get_file_service
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient, get
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.config import get_settings
from app.db.base import Base
from app.dependencies.database import get_db_session
from app.dependencies.user import get_user_service
from app.main import app

settings = get_settings()

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@study-buddy-db:5432/test_db",
)

test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool, future=True)

TestSessionLocal = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db() -> AsyncGenerator[None, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        async with session.begin():
            yield session
            await session.rollback()


@pytest_asyncio.fixture()
async def client(db_session: AsyncSession) -> AsyncIterator[AsyncClient]:
    app.dependency_overrides[get_db_session] = lambda: db_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def mock_file_service(client: AsyncClient) -> Generator[AsyncMock, None, None]:
    return get_file_service(client)
    # mock = AsyncMock()
    # app.dependency_overrides[get_file_service] = lambda: mock
    # yield mock
    # app.dependency_overrides.clear()


@pytest.fixture
def mock_user_service() -> Generator[AsyncMock, None, None]:
    mock = AsyncMock()
    app.dependency_overrides[get_user_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()
