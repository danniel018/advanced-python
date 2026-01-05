from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...services.user import UserService
from ..dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[BaseModel])
async def get_users(user_service: UserService = Depends(get_user_service)):
    result = await user_service.fetch_users()
    return result
