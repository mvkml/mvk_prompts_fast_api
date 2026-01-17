from   fastapi import Depends
from app.dal.dependencies_dal import get_map_user
from app.common.dependencies_common import get_user_validation_utility
from app.services.user_service import UserService
from app.dal.repositories.user_repository import UserRepository
from app.dal.connections.sql_connection import get_db



def get_user_repository(db = Depends(get_db), map_user = Depends(get_map_user)):
    user_repository = UserRepository(db, map_user)
    return user_repository


def get_user_service(user_repository = Depends(get_user_repository),
                     user_validation_utility = Depends(get_user_validation_utility)):
    return UserService(user_repository, user_validation_utility)
