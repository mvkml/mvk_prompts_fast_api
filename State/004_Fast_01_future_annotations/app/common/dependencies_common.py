from fastapi import Depends
from app.common.modules.users.user_validation_utility import UserValidationUtility

def get_user_validation_utility():
    return UserValidationUtility()