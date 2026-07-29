from pydantic import BaseModel, ConfigDict


class CreatedUserResponseModel(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)
