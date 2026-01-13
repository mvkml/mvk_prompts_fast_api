from app.services.user_service import UserService
from fastapi import APIRouter
from app.models.user_model import (UserModel,
                                   UserItem, UserRequest, UserResponse)


user_router = APIRouter()


@user_router.get("")
async def default_user():
    return {"response"," api "}


@user_router.post("/item")
async def get_user(request:UserRequest)->UserResponse:
    response = UserResponse()
    try:
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response






