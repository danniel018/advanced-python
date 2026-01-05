from abc import ABC, abstractmethod

from ..core.models import User

# Interfaces


class BaseUserRepository(ABC):
    @abstractmethod
    def add(self, item) -> User:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> User | None:
        pass

    @abstractmethod
    def get_all(self) -> list[User]:
        pass

    @abstractmethod
    def update(self, item) -> bool:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> bool:
        pass
