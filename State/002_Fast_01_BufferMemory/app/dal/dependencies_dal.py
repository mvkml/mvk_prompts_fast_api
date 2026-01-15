
from fastapi import Depends
from app.dal.utilities.module.map_user import MapUser

def get_map_user() -> MapUser:
    return MapUser()
