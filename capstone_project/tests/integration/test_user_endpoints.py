"""Integration tests for user API endpoints"""

import pytest
from httpx import ASGITransport, AsyncClient
from src.main import app


@pytest.fixture(scope="function")
async def async_client(override_get_session):
    """Create an async test client"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


class TestUserEndpoints:
    """Test suite for user API endpoints"""

    @pytest.mark.asyncio
    async def test_get_users_empty_list(self, async_client):
        """Test GET /users endpoint returns empty list initially"""
        response = await async_client.get("/api/v1/users/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0

    @pytest.mark.asyncio
    async def test_get_users_endpoint_accessible(self, async_client):
        """Test that users endpoint is accessible"""
        response = await async_client.get("/api/v1/users/")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
