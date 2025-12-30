from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from ..dependencies import get_user_service
from ...services.user import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[BaseModel])
async def get_users(user_service: UserService = Depends(get_user_service)):
    result = await user_service.fetch_users()
    return result
