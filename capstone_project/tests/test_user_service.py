"""Unit tests for UserService."""

import pytest

from capstone_project.src.core.models import User
from capstone_project.src.repositories.base import BaseUserRepository
from capstone_project.src.services.user import UserService


class MockUserRepository(BaseUserRepository):
    """Mock repository for testing UserService."""

    def __init__(self):
        self.users = []
        self.next_id = 1

    async def add(self, item: dict) -> User:
        user = User(
            id=self.next_id,
            username=item["username"],
            email=item["email"],
            age=item["age"],
        )
        self.users.append(user)
        self.next_id += 1
        return user

    async def get_by_id(self, item_id: int):
        for user in self.users:
            if user.id == item_id:
                return user
        return None

    async def get_all(self):
        return self.users

    async def update(self, item: User) -> bool:
        for i, user in enumerate(self.users):
            if user.id == item.id:
                self.users[i] = item
                return True
        return False

    async def delete(self, item_id: int) -> bool:
        for i, user in enumerate(self.users):
            if user.id == item_id:
                del self.users[i]
                return True
        return False


@pytest.mark.asyncio
async def test_register_user():
    """Test user registration."""
    # Arrange
    mock_repo = MockUserRepository()
    user_service = UserService(mock_repo)

    # Act
    result = await user_service.register_user(
        username="testuser",
        email="test@example.com",
        age=25,
    )

    # Assert
    assert result.id == 1
    assert result.username == "testuser"
    assert result.email == "test@example.com"
    assert result.age == 25


@pytest.mark.asyncio
async def test_fetch_users():
    """Test fetching all users."""
    # Arrange
    mock_repo = MockUserRepository()
    user_service = UserService(mock_repo)
    await user_service.register_user("user1", "user1@example.com", 20)
    await user_service.register_user("user2", "user2@example.com", 30)

    # Act
    result = await user_service.fetch_users()

    # Assert
    assert len(result) == 2
    assert result[0].username == "user1"
    assert result[1].username == "user2"


@pytest.mark.asyncio
async def test_fetch_users_empty():
    """Test fetching users when repository is empty."""
    # Arrange
    mock_repo = MockUserRepository()
    user_service = UserService(mock_repo)

    # Act
    result = await user_service.fetch_users()

    # Assert
    assert len(result) == 0
