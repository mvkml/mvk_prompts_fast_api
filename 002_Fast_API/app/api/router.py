from fastapi import APIRouter
from api.api_pt.api_pt import router as api_pt_router

api_router = APIRouter()
api_router.include_router(api_pt_router, prefix="/api_pt")

