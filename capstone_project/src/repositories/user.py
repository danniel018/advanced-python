from ..db.models import UserModel
from ..core.models import User
from .base import BaseUserRepository
from typing import Optional, List

class SQLAlchemyUserRepository(BaseUserRepository):
    def __init__(self, session):
        self.session = session

    def add(self, item: dict) -> User:
        user = UserModel(
            username=item['username'],
            email=item['email'],
            age=item['age']
        )       
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        self._to_domain_model(user)
        return user
    
    def _to_domain_model(self, user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            age=user_model.age
        )
    
    def _to_orm_model(self, user: User) -> UserModel:
        return UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            age=user.age
        )
    
    def get_by_id(self, item_id: int) -> Optional[User]:
        user_model = self.session.query(UserModel).filter(UserModel.id == item_id).first()
        if user_model:
            return self._to_domain_model(user_model)
        return None

    def get_all(self) -> List[User]:
        user_models = self.session.query(UserModel).all()
        return [self._to_domain_model(user_model) for user_model in user_models]

    def update(self, item: User) -> bool:
        existing_user = self.get_by_id(item.id)
        if not existing_user:
            return False
        existing_user.username = item.username
        existing_user.email = item.email
        existing_user.age = item.age
        self.session.commit()
        return True

    def delete(self, item_id: int) -> bool:
        user = self.get_by_id(item_id)
        if not user:
            return False
        self.session.delete(user)
        self.session.commit()
        return True
    