"""module for domain logic for user service"""

from ..core.models import User
from ..repositories.base import BaseUserRepository


class UserService:
    def __init__(self, user_repository: BaseUserRepository) -> None:
        self.repository = user_repository

    def register_user(self, username: str, email: str, age: int) -> User:
        # domain logic for registering a user
        # e.g., call methods for user age validation

        new_user = User(id=None, username=username, email=email, age=age)
        return self.repository.add(new_user)
