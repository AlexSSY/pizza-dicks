import pytest
from pydantic import BaseModel, ValidationError

from pydantic_ext import PydanticTypes


class Model(BaseModel):
    password: PydanticTypes.Password


def test_accepts_valid_password():
    model = Model(password="Password!")

    assert model.password == "Password!"


@pytest.mark.parametrize(
    "password",
    [
        "",
        "1234567",
        "Pass1!",
    ],
)
def test_rejects_short_password(password):
    with pytest.raises(ValidationError):
        Model(password=password)


def test_rejects_password_without_uppercase():
    with pytest.raises(ValidationError):
        Model(password="password!")


def test_rejects_password_without_special_character():
    with pytest.raises(ValidationError):
        Model(password="Password")


def test_accepts_minimum_length_password():
    model = Model(password="Passw0r!")

    assert model.password == "Passw0r!"


def test_rejects_too_long_password():
    password = "A!" + "a" * 100

    with pytest.raises(ValidationError):
        Model(password=password)