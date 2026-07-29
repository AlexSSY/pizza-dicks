import pytest
from httpx import ASGITransport, AsyncClient

from depends import get_register_user_uow
from main import app
from models import User
from response_models import CreatedUserResponseModel


class FakeRegisterUserUow:
    def __init__(self):
        self.email = None
        self.password = None

    async def __call__(self, email: str, password: str) -> User:
        self.email = email
        self.password = password
        created_user = User(id=1, email=self.email, hashed_password=self.password).__dict__
        return created_user


fake_uow = FakeRegisterUserUow()
app.dependency_overrides[get_register_user_uow] = (
    lambda: fake_uow
)


async def test_valid_request(test_client: AsyncClient):
    response = await test_client.post(
        '/users/register',
        json={
            'email': 'robert@mail.com',
            'password': 'Password123!',
            'password_confirmation': 'Password123!'
        }
    )

    assert response.status_code == 201
    assert fake_uow.email == "robert@mail.com"
    assert fake_uow.password == "Password123!"


async def test_missing_email(test_client: AsyncClient):
    response = await test_client.post(
        '/users/register',
        json={
            'password': 'Password123!',
            'password_confirmation': 'Password123!'
        }
    )

    assert response.status_code == 422
    assert 'email' in response.text
    assert 'missing' in response.text
    assert 'required' in response.text


async def test_missing_password(test_client: AsyncClient):
    response = await test_client.post(
        '/users/register',
        json={
            'email': 'robert@mail.com',
            'password_confirmation': 'Password123!'
        }
    )

    assert response.status_code == 422
    assert 'password' in response.text
    assert 'missing' in response.text
    assert 'required' in response.text


async def test_missing_password_confirmation(test_client: AsyncClient):
    response = await test_client.post(
        '/users/register',
        json={
            'email': 'robert@mail.com',
            'password': 'Password123!'
        }
    )

    assert response.status_code == 422
    assert 'password_confirmation' in response.text
    assert 'missing' in response.text
    assert 'required' in response.text
