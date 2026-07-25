from fastapi.applications import FastAPI
from fastapi.params import Body

from register_user import RegisterUserUnitOfWork
from request_models import RegisterUserRequestModel


app = FastAPI(debug=True)


@app.post("register/")
def register_traffic_controller(
    register_user_request: RegisterUserRequestModel = Body(...)
):
    pass


if __name__ == "__main__":
    print("Please don't run!!!")
