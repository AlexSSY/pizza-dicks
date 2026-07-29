from datetime import UTC, datetime, timedelta
from typing import Annotated, TypedDict, cast

import jwt
from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse
from jwt import InvalidTokenError
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from depends import DbSession
from interfaces import PasswordHasher
from models import User
from repositories import UserRepository
from security import BCryptPasswordHasher
from settings import settings


class LoginRequestModel(BaseModel):
    email: EmailStr
    password: str


class LoginResponseModel(BaseModel):
    access_token: str


class AuthenticationError(Exception):
    pass


type JsonWebToken = str


class JwtPayload(TypedDict):
    sub: str
    exp: datetime


class AuthenticationService:
    def __init__(self, session: AsyncSession):
        self._session = session

    def generate_access_token(self, user: User) -> JsonWebToken:
        return jwt.encode(
            payload={
                "sub": str(user.id), "exp": datetime.now(UTC) + timedelta(hours=1)
            },
            key=settings.secret_key,
            algorithm="HS256",
        )

    async def get_user(self, access_token: JsonWebToken) -> User:
        try:
            jwt_payload = cast(
                JwtPayload,
                jwt.decode(
                    jwt=access_token,
                    key=settings.secret_key,
                    algorithms=["HS256"],
                ),
            )
        except InvalidTokenError as exc:
            raise AuthenticationError() from exc

        user_repo = UserRepository(session=self._session)
        user = await user_repo.find_by_id(id=int(jwt_payload["sub"]))
        if user is None:
            raise AuthenticationError()

        return user


class AuthenticateUserUnitOfWork:
    def __init__(self, session: AsyncSession, password_hasher: PasswordHasher):
        self._session = session
        self._password_hasher = password_hasher

    async def __call__(self, email: str, password: str) -> User:
        user_repo = UserRepository(self._session)
        user = await user_repo.find_by_email(email=email)
        if user is None:
            raise AuthenticationError()
        if not self._password_hasher.verify(
            raw_password=password, hashed_password=user.hashed_password
        ):
            raise AuthenticationError()

        return user


def get_auth_user_uow(session: DbSession) -> AuthenticateUserUnitOfWork:
    return AuthenticateUserUnitOfWork(
        session=session, password_hasher=BCryptPasswordHasher()
    )


AuthUserDep = Annotated[AuthenticateUserUnitOfWork, Depends(get_auth_user_uow)]


def get_auth_service(session: DbSession) -> AuthenticationService:
    return AuthenticationService(session=session)


AuthServiceDep = Annotated[AuthenticationService, Depends(get_auth_service)]


async def get_access_token(
    authorization: Annotated[str, Header(alias="Authorization")],
) -> JsonWebToken:
    scheme, _, token = authorization.partition(" ")

    if scheme != "Bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return token


async def get_current_user(
    auth_service: AuthServiceDep,
    access_token: Annotated[JsonWebToken, Depends(get_access_token)],
):
    return await auth_service.get_user(access_token=access_token)


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AuthenticationError)
    async def user_exists_handler(request: Request, exc: AuthenticationError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid Credentials."},
        )



router = APIRouter(prefix="/auth")


@router.post("/login")
async def login_traffic_controller(
    login_request_model: LoginRequestModel,
    auth_user: AuthUserDep,
    auth_service: AuthServiceDep,
) -> LoginResponseModel:
    user = await auth_user(
        email=login_request_model.email, password=login_request_model.password
    )
    access_token = auth_service.generate_access_token(user=user)
    return LoginResponseModel(access_token=access_token)
