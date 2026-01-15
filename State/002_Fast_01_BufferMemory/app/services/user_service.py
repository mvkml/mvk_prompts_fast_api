from app.models.user_model import (
    UserModel,
    UserItem,
    UserResponse
    )
from fastapi import Depends
from app.dal.repositories.user_repository import UserRepository
from app.common.modules.users.user_validation_utility import UserValidationUtility
    

class UserService():
    def __init__(self, user_repository: UserRepository, user_validation_utility:UserValidationUtility):
        self.user_repository = user_repository
        self.user_validation_utility = user_validation_utility

    def set_response(self, model: UserModel) -> UserModel:
        if model.IsInvalid:
            response = UserResponse()
            response.IsInvalid = True
            response.Message = model.Message
            model.response = response
        else:
            response = UserResponse(
                UserId=model.item.UserId if model.item else 0,
                Name=model.item.Name if model.item else "",
                Message="User created successfully"
            )
            model.response = response
        return model
        
    def create_user(self, model: UserModel) -> UserModel:
        model = self.user_validation_utility.validate_user_model(model)
        
        if model.IsInvalid:
            model = self.set_response(model)
            return model
        
        model =  self.user_repository.create_user(model)
        model = self.set_response(model)
        return model