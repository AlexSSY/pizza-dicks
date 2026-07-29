from fastapi.applications import FastAPI

from auth import router as auth_router, register_exception_handlers as auth_register_exception_handlers
from db import engine
from infrastructure import CreateAllTablesUnitOfWork
from models import Base
from users import register_exception_handlers, users_router


async def lifespan(app: FastAPI):
    await CreateAllTablesUnitOfWork(engine=engine, metadata=Base.metadata).do()
    yield


app = FastAPI(debug=True, lifespan=lifespan)
register_exception_handlers(app)
auth_register_exception_handlers(app)
app.include_router(users_router)
app.include_router(auth_router)


if __name__ == "__main__":
    print("Please don't run!!!")
