from abc import ABC, abstractmethod

from ..core.models import User

# Interfaces


class BaseUserRepository(ABC):
    @abstractmethod
    async def add(self, item) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, item_id: int) -> User | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[User]:
        pass

    @abstractmethod
    async def update(self, item) -> bool:
        pass

    @abstractmethod
    async def delete(self, item_id: int) -> bool:
        pass
