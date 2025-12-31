"""Pytest configuration and fixtures for testing."""

import asyncio
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from capstone_project.src.db.models import Base
from capstone_project.src.main import app

# Create test database engine
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_capstone.db"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

test_async_session = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the entire test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session for each test."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Provide session
    async with test_async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with a test database session."""
    from capstone_project.src.db.session import get_session_db

    # Override the database session dependency
    async def override_get_session_db():
        yield db_session

    app.dependency_overrides[get_session_db] = override_get_session_db

    # Create test client
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    # Clear overrides
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Provide sample user data for testing."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "age": 25,
    }
