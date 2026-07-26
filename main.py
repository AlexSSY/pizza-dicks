from fastapi.applications import FastAPI
from fastapi.responses import Response

from register_user import RegisterUserStatus
from request_models import RegisterUserRequestModel
from infrastructure import CreateAllTablesUnitOfWork
from db import engine
from models import Base
from depends import RegisterUserUow


async def lifespan(app: FastAPI):
    await CreateAllTablesUnitOfWork(engine=engine, metadata=Base.metadata).do()
    yield


app = FastAPI(debug=True, lifespan=lifespan)


@app.post("register/")
async def register_traffic_controller(
    register_user_request: RegisterUserRequestModel,
    register_user: RegisterUserUow
):
    result = await register_user(email=register_user_request.email, password=register_user_request.password)
    match result:
        case RegisterUserStatus.ALREADY_EXISTS:
            pass

    return Response(status_code=201)


if __name__ == "__main__":
    print("Please don't run!!!")
