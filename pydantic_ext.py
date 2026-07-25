from typing import Annotated
from pydantic import AfterValidator

from security import PasswordValidator


class PydanticTypes:
    Password = Annotated[
        str,
        AfterValidator(PasswordValidator()),
    ]
