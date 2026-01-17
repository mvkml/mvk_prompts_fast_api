# app/api/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session
from app.dal.connections.sql_connection import get_db
from app.dal.repositories.user_repository import UserRepository

def get_user_repo(db: Session = Depends(get_db)):
    return UserRepository(db)
