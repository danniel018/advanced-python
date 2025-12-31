from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ..dependencies import get_user_service
from ...services.user import UserService


router = APIRouter(prefix="/users", tags=["users"])


class UserResponse(BaseModel):
    """Response model for user data."""

    id: int
    username: str
    email: str
    age: int

    class Config:
        from_attributes = True


@router.get("/", response_model=List[UserResponse])
async def get_users(user_service: UserService = Depends(get_user_service)):
    """Get all users."""
    result = await user_service.fetch_users()
    # Convert domain models to response models
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            age=user.age,
        )
        for user in result
    ]

