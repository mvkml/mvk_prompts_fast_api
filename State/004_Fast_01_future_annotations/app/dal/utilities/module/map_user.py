from app.models.user_model import(
    UserItem,UserModel,UserRequest,UserResponse,UserResponses
)
from app.dal.entities.User import (UserEntity)


class MapUser():
    def __init__(self):
        pass

    def UserItemToEntity(self, source: UserItem) -> UserEntity:
        destination = UserEntity()
        destination.Id = source.Id
        destination.UserId = source.UserId
        destination.Name = source.Name
        return destination
        
    def UserEntityToItem(self, source: UserEntity) -> UserItem:
        destination = UserItem()
        destination.Id = source.Id
        destination.Name = source.Name
        destination.UserId = source.UserId
        return destination