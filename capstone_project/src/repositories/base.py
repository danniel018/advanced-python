from abc import ABC, abstractmethod
from ..core.models import User
from typing import Optional, List
#Interfaces


class BaseUserRepository(ABC):
    @abstractmethod
    def add(self, item) -> User:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_all(self) -> List[User]: 
        pass

    @abstractmethod
    def update(self, item) -> bool:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> bool:
        pass