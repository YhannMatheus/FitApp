from passlib.context import CryptContext


class Password:
    _context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, raw: str) -> str:
        return cls._context.hash(raw)

    @classmethod
    def verify(cls, raw: str, hashed: str) -> bool:
        return cls._context.verify(raw, hashed)
