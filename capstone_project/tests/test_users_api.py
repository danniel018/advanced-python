"""Integration tests for the users API endpoint."""

import pytest
from httpx import AsyncClient

from capstone_project.src.db.models import UserModel


@pytest.mark.asyncio
async def test_get_users_empty(client: AsyncClient):
    """Test GET /users endpoint when no users exist."""
    response = await client.get("/api/v1/users/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_users_with_data(client: AsyncClient, db_session, sample_user_data):
    """Test GET /users endpoint with existing users."""
    # Add test data to database
    user1 = UserModel(username="user1", email="user1@example.com", age=25)
    user2 = UserModel(username="user2", email="user2@example.com", age=30)
    db_session.add_all([user1, user2])
    await db_session.commit()

    # Make request
    response = await client.get("/api/v1/users/")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["username"] == "user1"
    assert data[0]["email"] == "user1@example.com"
    assert data[0]["age"] == 25
    assert data[1]["username"] == "user2"
    assert data[1]["email"] == "user2@example.com"
    assert data[1]["age"] == 30
