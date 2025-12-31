from abc import ABC, abstractmethod
from typing import List, Optional

from ..core.models import User

# Interfaces


class BaseUserRepository(ABC):
    @abstractmethod
    async def add(self, item) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, item_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_all(self) -> List[User]:
        pass

    @abstractmethod
    async def update(self, item) -> bool:
        pass

    @abstractmethod
    async def delete(self, item_id: int) -> bool:
        pass
