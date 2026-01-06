import json
from fastapi import APIRouter
from app.core.config import Settings, settings 
 

''' wirte a comment'''
api_pt_router = APIRouter()

'''
/api_pt
'''
@api_pt_router.get("/")
async def get_default_async():
    return {"message": "Default response from api_pt"}

@api_pt_router.get("/config")
async def get_status():
    var_settings = {
        "env": settings.env,
        "open_ai_key": settings.open_ai_key,
        "app_name": settings.app_name,
        "host": settings.host,
        "port": settings.port,
        "db_host": settings.db_host,
        "db_port": settings.db_port,
        "db_name": settings.db_name,
        "db_user": settings.db_user,
        "db_password": settings.db_password,
        "log_level": settings.log_level,
    }
    return var_settings

@api_pt_router.get("/prompt")
async def get_prompt(prompt: str):
    return {"prompt": prompt}   