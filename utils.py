class FakePasswordHasher:
    def hash(self, raw_password: str) -> str:
        return f"hashed:{raw_password}"

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return hashed_password == f"hashed:{raw_password}"