"""module for domain logic for user service"""

from ..core.models import User
from ..repositories.base import BaseUserRepository


class UserService:
    """Domain logic for user-related operations"""
    def __init__(self, user_repository: BaseUserRepository) -> None:
        self.repository = user_repository

    def _check_age_constraints(self, age: int) -> bool:
        # domain logic for age constraints
        return 0 < age < 150

    def register_user(self, username: str, email: str, age: int) -> User:
        # domain logic for registering a user
        # e.g., call methods for user age validation
        if not self._check_age_constraints(age):
            raise ValueError("Age must be between 1 and 149")

        new_user = User(id=None, username=username, email=email, age=age)
        return self.repository.add(new_user)

    async def fetch_users(self) -> list[User]:
        # domain logic for fetching users
        return await self.repository.get_all()
