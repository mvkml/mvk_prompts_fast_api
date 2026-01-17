from typing_extensions import Annotated
from app.dal.entities import User
from app.models.user_model import UserModel
from fastapi import Depends
from sqlalchemy.orm import session
from app.dal.connections.sql_connection import get_db

from app.dal.utilities.module.map_user import MapUser
from app.dal.dependencies_dal import get_map_user
from app.dal.entities.User import UserEntity


class UserRepository():
    def __init__(self,db: session,map_user: MapUser):
        self.db = db
        self.map_user = map_user

    def set_inv_msg(self, model: UserModel, msg: str) -> UserModel:
        model.IsInvalid = True
        model.Message = msg
        return model

    def create_user(self,model: UserModel)->UserModel:
        try:
            if self.db == None:
                model = self.set_inv_msg(model=model,msg="Database session is None")
                return model
            # entity = self.map_user.UserItemToEntity(model.item)
            entity = UserEntity(UserId=model.item.UserId, Name=model.item.Name)
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            model.item = self.map_user.UserEntityToItem(entity)
            return model
        except Exception as ex:
            model = self.set_inv_msg(model=model,msg=str(ex))
        return model
    
 
