from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_session_db
from ..repositories.user import SQLAlchemyUserRepository
from ..services.user import UserService


def get_user_service(
    session: AsyncSession = Depends(get_session_db),
) -> UserService:
    user_repository = SQLAlchemyUserRepository(session)
    user_service = UserService(user_repository)
    return user_service
