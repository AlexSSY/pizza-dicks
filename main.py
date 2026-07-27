from fastapi.applications import FastAPI

from infrastructure import CreateAllTablesUnitOfWork
from db import engine
from models import Base
from users import users_router


async def lifespan(app: FastAPI):
    await CreateAllTablesUnitOfWork(engine=engine, metadata=Base.metadata).do()
    yield


app = FastAPI(debug=True, lifespan=lifespan)
app.include_router(users_router)


if __name__ == "__main__":
    print("Please don't run!!!")
