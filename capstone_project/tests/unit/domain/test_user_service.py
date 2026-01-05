"""Unit tests for UserService domain logic"""

from unittest.mock import Mock

import pytest
from src.core.models import User
from src.services.user import UserService


@pytest.fixture
def mock_repository():
    """Create a mock repository for testing"""
    return Mock()


@pytest.fixture
def user_service(mock_repository):
    """Create UserService instance with mock repository"""
    return UserService(mock_repository)


class TestUserServiceRegistration:
    """Test suite for user registration logic"""

    def test_register_user_success(self, user_service, mock_repository):
        """Test successful user registration"""
        # Arrange
        new_user = User(id=1, username="john", email="john@test.com", age=25)
        mock_repository.add.return_value = new_user

        # Act
        result = user_service.register_user("john", "john@test.com", 25)

        # Assert
        assert result.username == "john"
        assert result.email == "john@test.com"
        assert result.age == 25
        mock_repository.add.assert_called_once()

    def test_register_user_calls_repository_with_user_model(self, user_service, mock_repository):
        """Test that repository is called with User domain model"""
        # Arrange
        mock_repository.add.return_value = User(
            id=1, username="jane", email="jane@test.com", age=30
        )

        # Act
        user_service.register_user("jane", "jane@test.com", 30)

        # Assert
        called_user = mock_repository.add.call_args[0][0]
        assert isinstance(called_user, User)
        assert called_user.username == "jane"
        assert called_user.email == "jane@test.com"
        assert called_user.age == 30
        assert called_user.id is None  # ID should be None before persistence

    def test_register_user_with_different_ages(self, user_service, mock_repository):
        """Test user registration with various age values"""
        # Arrange
        test_cases = [18, 25, 50, 100]

        for age in test_cases:
            mock_user = User(id=1, username="testuser", email="test@test.com", age=age)
            mock_repository.add.return_value = mock_user

            # Act
            result = user_service.register_user("testuser", "test@test.com", age)

            # Assert
            assert result.age == age
            mock_repository.add.reset_mock()

    def test_register_user_returns_repository_result(self, user_service, mock_repository):
        """Test that service returns what repository returns"""
        # Arrange
        expected_user = User(id=99, username="bob", email="bob@example.com", age=40)
        mock_repository.add.return_value = expected_user

        # Act
        result = user_service.register_user("bob", "bob@example.com", 40)

        # Assert
        assert result is expected_user
