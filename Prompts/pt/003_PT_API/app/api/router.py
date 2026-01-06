from fastapi import APIRouter
from app.api.api_pt.api_pt import api_pt_router

api_router = APIRouter()
api_router.include_router(api_pt_router, prefix="/api_pt")

