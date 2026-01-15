from app.services.user_service import UserService
from fastapi import APIRouter
from typing import Annotated
from app.models.user_model import (UserModel,
                                   UserItem, UserRequest, UserResponse, UserResponses)
from app.services.user_service import UserService
from fastapi import Depends
from app.api.dependencies import get_user_service
from app.common.dependencies_common import get_user_validation_utility

di_user_service = Annotated[UserService, Depends(get_user_service)]

user_router = APIRouter()

@user_router.get("")
async def default_user():
    return {"response"," api "}


@user_router.get("/get/user")
async def get_user(request:UserRequest=Depends())->UserResponse:
    response = UserResponses()
    try:
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response


@user_router.post("/get/users")
async def get_user(request:UserRequest=Depends())->UserResponse:
    response = UserResponses()
    try:
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response

@user_router.post("/update/user")
async def update_user(request:UserRequest=Depends())->UserResponse:
    response = UserResponse()
    try:
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response


@user_router.post("/create/user")
async def create_user(request:UserRequest,service:di_user_service)->UserResponse:
    response = UserResponse()
    try:
        validation_utility = get_user_validation_utility()
        model = UserModel()
        model.request = request

        model = validation_utility.validate_user_request(model=model)

        if model.IsInvalid:
            response.IsInvalid = model.IsInvalid
            response.Message = model.Message
            return response
        
        model = service.create_user(model)
        response = model.response
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response



@user_router.post("/delete/user")
async def delete_user(request:UserRequest)->UserResponse:
    response = UserResponse()
    try:
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response


@user_router.post("/upsert/user")
async def upsert_user(request:UserRequest)->UserResponse:
    response = UserResponse()
    try:
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response


