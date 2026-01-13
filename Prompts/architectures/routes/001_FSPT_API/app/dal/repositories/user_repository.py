from app.models.user_model import UserModel
from fastapi import Depends
from sqlalchemy.orm import session
from app.dal.connections.sql_connection import get_db

class UserRepository():
    def __init__(self,db: session):
        self.db = db

    def create_user(self,model: UserModel)->UserModel:
        return model
    
 
