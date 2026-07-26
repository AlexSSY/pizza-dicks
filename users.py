from fastapi import status
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRouter

from depends import RegisterUserUow
from register_user import UserAlreadyExistsError
from request_models import RegisterUserRequestModel

users_router = APIRouter(prefix="/users")


@users_router.exception_handler(UserAlreadyExistsError)
async def user_exists_handler(request, exc):
    return JSONResponse(
        status_code=409,
        content={"detail": "User already exists"},
    )


@users_router.post("/register")
async def register_traffic_controller(
    register_user_request: RegisterUserRequestModel, register_user: RegisterUserUow
):
    await register_user(
        email=register_user_request.email, password=register_user_request.password
    )

    return Response(status_code=status.HTTP_201_CREATED)


# POST /users/auth