

from typing import Optional
from app.models.common.common_base import (
                                        ItemBase,RequestBase,ResponseBase
                                      )
class UserItem(ItemBase):
    Id:int=0
    Name:str=""

class UserRequest(RequestBase):
    Id:int=0
    Name:str=""

class UserResponse(ResponseBase):
    Id:int=0
    Name:str=""

class UserModel():
    item:Optional[UserItem]=None
 
    
 

