"""Shared test fixtures for the test suite"""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Base
from src.db.session import get_session_db


@pytest_asyncio.fixture
async def async_engine():
    """Create a test database engine using in-memory SQLite"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def async_session(async_engine):
    """Create a test database session"""
    async_session_local = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_local() as session:
        yield session


@pytest.fixture
def override_get_session(async_session):
    """Override FastAPI dependency injection for testing"""
    from src.main import app

    async def get_test_session():
        yield async_session

    app.dependency_overrides[get_session_db] = get_test_session
    yield
    app.dependency_overrides.clear()
