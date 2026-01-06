import json
from fastapi import APIRouter


router = APIRouter()

'''
/api_pt
'''
@router.get("/")
async def get_default_async():
    return {"message": "Default response from api_pt"}










