from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass


# Domain model
@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    age: int


# Repository interface
class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> bool:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass


# Concrete implementation - In-memory storage
class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = {}
        self._next_id = 1

    def add(self, user: User) -> User:
        user.id = self._next_id
        self._users[self._next_id] = user
        self._next_id += 1
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def get_all(self) -> List[User]:
        return list(self._users.values())

    def update(self, user: User) -> bool:
        if user.id in self._users:
            self._users[user.id] = user
            return True
        return False

    def delete(self, user_id: int) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False


# Concrete implementation - SQLite (simulated)
class SQLiteUserRepository(UserRepository):
    def __init__(self, connection):
        self.conn = connection
        self._create_table()

    def _create_table(self):
        # Simplified - would use actual SQL
        print("Creating users table in SQLite...")

    def add(self, user: User) -> User:
        # Would execute: INSERT INTO users ...
        print(f"Inserting {user.username} into SQLite")
        user.id = 1  # Would get from database
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        # Would execute: SELECT * FROM users WHERE id = ?
        print(f"Querying SQLite for user ID {user_id}")
        return None

    def get_by_username(self, username: str) -> Optional[User]:
        print(f"Querying SQLite for username {username}")
        return None

    def get_all(self) -> List[User]:
        print("Fetching all users from SQLite")
        return []

    def update(self, user: User) -> bool:
        print(f"Updating user {user.id} in SQLite")
        return True

    def delete(self, user_id: int) -> bool:
        print(f"Deleting user {user_id} from SQLite")
        return True


# Business logic layer - doesn't know about storage details
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, username: str, email: str, age: int) -> User:
        # Business validation
        if age < 18:
            raise ValueError("User must be 18 or older")

        # Check if username exists
        existing = self.repository.get_by_username(username)
        if existing:
            raise ValueError("Username already taken")

        # Create and save user
        user = User(id=None, username=username, email=email, age=age)
        return self.repository.add(user)

    def get_adult_users(self) -> List[User]:
        all_users = self.repository.get_all()
        return [u for u in all_users if u.age >= 18]


# Usage
if __name__ == "__main__":
    # Use in-memory repository
    print("=== Using In-Memory Repository ===")
    repo = InMemoryUserRepository()
    service = UserService(repo)

    user1 = service.register_user("alice", "alice@example.com", 25)
    user2 = service.register_user("bob", "bob@example.com", 30)

    print(f"Created: {user1}")
    print(f"All users: {service.get_adult_users()}")

    # Switch to SQLite - business logic unchanged!
    print("\n=== Switching to SQLite Repository ===")
    sqlite_repo = SQLiteUserRepository(connection=None)
    service2 = UserService(sqlite_repo)

    service2.register_user("charlie", "charlie@example.com", 28)
