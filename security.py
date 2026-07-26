import re

import bcrypt


class PasswordValidator:
    def __init__(
        self,
        *,
        min_length: int = 8,
        max_length: int = 64,
        require_uppercase: bool = True,
        require_special: bool = True,
    ):
        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_special = require_special

    def __call__(self, password: str) -> str:
        if len(password) < self.min_length:
            raise ValueError(
                f"Password must contain at least {self.min_length} characters."
            )

        if len(password) > self.max_length:
            raise ValueError(
                f"Password must contain at most {self.max_length} characters."
            )

        if self.require_uppercase and not any(c.isupper() for c in password):
            raise ValueError(
                "Password must contain an uppercase letter."
            )

        if self.require_special and not re.search(r"[^\w\s]", password):
            raise ValueError(
                "Password must contain a special character."
            )

        return password


class BCryptPasswordHasher:
    def hash(self, raw_password: str) -> str:
        password_bytes = raw_password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password

    
    def verify(self, raw_password: str, hashed_password: str) -> bool:
        password_bytes = raw_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_password)
