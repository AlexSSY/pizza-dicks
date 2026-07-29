from pydantic import BaseModel, EmailStr, model_validator

from pydantic_ext import PydanticTypes


class RegisterUserRequestModel(BaseModel):
    email: EmailStr
    password: PydanticTypes.Password
    password_confirmation: str

    @model_validator(mode='after')
    def verify_passwords_match(self):
        if self.password != self.password_confirmation:
            raise ValueError('Passwords do not match')
        return self
