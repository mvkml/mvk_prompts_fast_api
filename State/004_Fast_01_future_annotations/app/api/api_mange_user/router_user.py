from fastapi import APIRouter
from app.api.api_mange_user import api_user
module_user_router = APIRouter(prefix="/manage", tags=["User"])
module_user_router.include_router(api_user.user_router,prefix="/user")