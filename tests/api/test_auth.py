import pytest
from httpx import AsyncClient

from main import app
from models import User
from auth import JsonWebToken, get_auth_user_uow, get_auth_service, AuthenticationError


class FakeAuthenticationService:
    def generate_access_token(self, user: User) -> JsonWebToken:
        return 'roi de musca'

    async def get_user(self, access_token: JsonWebToken) -> User:
        return User(id=1, email="robert@mlunu.ua", hashed_password='spagetti')


class FakeAuthenticateUserUnitOfWork:
    async def __call__(self, email: str, password: str) -> User:
        if email == "robert@mlunu.ua" and password == "spagetti":
            return User(id=1, email="robert@mlunu.ua", hashed_password='hashed_spagetti')
        raise AuthenticationError()


app.dependency_overrides[get_auth_service] = lambda: FakeAuthenticationService()
app.dependency_overrides[get_auth_user_uow] = lambda: FakeAuthenticateUserUnitOfWork()


@pytest.mark.asyncio
async def test_auth_tc(test_client: AsyncClient):
    response = await test_client.post(
        '/auth/login',
        json={
            'email': 'robert@mlunu.ua',
            'password': 'spagetti',
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "roi de musca"
    }


@pytest.mark.asyncio
async def test_wrong_credentials(test_client: AsyncClient):
    response = await test_client.post(
        "/auth/login",
        json={
            "email": "wrong@mail.com",
            "password": "wrong",
        },
    )

    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid Credentials.'}
