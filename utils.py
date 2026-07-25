class FakePasswordHasher:
    def hash(self, raw_password: str) -> str:
        return raw_password
    
    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return raw_password == hashed_password
