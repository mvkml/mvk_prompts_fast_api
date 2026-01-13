from app.models.user_model import (
    UserModel,
    UserItem
    )
from fastapi import Depends
from app.dal.repositories.user_repository import UserRepository
from app.dal.repositories.dependencies import get_user_repo


class UserService():
    def __init__(self, user_repository: UserRepository = Depends(get_user_repo)):
        self.user_repository = user_repository

    def create_user(self, model: UserModel) -> UserModel:
        return self.user_repository.create_user(model)

