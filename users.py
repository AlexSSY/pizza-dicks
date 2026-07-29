from fastapi import status
from fastapi.applications import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from depends import RegisterUserUow
from register_user import UserAlreadyExistsError
from request_models import RegisterUserRequestModel
from response_models import CreatedUserResponseModel

users_router = APIRouter(prefix="/users")


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(UserAlreadyExistsError)
    async def user_exists_handler(request: Request, exc: UserAlreadyExistsError):
        return JSONResponse(
            status_code=409,
            content={"detail": "User already exists"},
        )


@users_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_traffic_controller(
    register_user_request: RegisterUserRequestModel, register_user: RegisterUserUow
) -> CreatedUserResponseModel:
    registered_user = await register_user(
        email=register_user_request.email, password=register_user_request.password
    )

    return CreatedUserResponseModel.model_validate(registered_user)


# POST /users/auth