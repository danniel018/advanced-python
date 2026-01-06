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
        assert isinstance(result, User)
        assert result.username == "john"
        assert result.email == "john@test.com"
        assert result.age == 25
        mock_repository.add.assert_called_once()


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

    def test_incorrect_age_value(self, user_service):
        """Test registration with incorrect age values"""
        # Arrange
        invalid_ages = [-5, 0, 150, 200]

        for age in invalid_ages:
            # Act & Assert
            with pytest.raises(ZeroDivisionError) as exc_info:
                user_service.register_user("invaliduser", "invalid@test.com", age)
            assert str(exc_info.value) == "Age must be between 1 and 149"
