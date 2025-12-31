"""module for domain logic for user service"""


from ..core.models import User
from ..repositories.base import BaseUserRepository


class UserService:
    def __init__(self, user_repository: BaseUserRepository) -> None:
        self.repository = user_repository

    async def register_user(self, username: str, email: str, age: int) -> User:
        # domain logic for registering a user
        # e.g., call methods for user age validation

        new_user_dict = {"username": username, "email": email, "age": age}
        return await self.repository.add(new_user_dict)

    async def fetch_users(self):
        """Fetch all users from repository."""
        return await self.repository.get_all()

