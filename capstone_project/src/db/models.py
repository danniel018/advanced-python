"""module to define database models with SQLAlchemy ORM"""

from typing import Any

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base: Any = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)  # type: ignore
    username: str = Column(String, unique=True, index=True, nullable=False)  # type: ignore
    email: str = Column(String, unique=True, index=True, nullable=False)  # type: ignore
    age: int = Column(Integer, nullable=False)  # type: ignore
