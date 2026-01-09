from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


class Authenticate:
    _context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    _oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    @classmethod
    def hash_password(cls, raw: str) -> str:
        """Hash a password using bcrypt"""
        # Bcrypt tem limite de 72 bytes - truncar antes de processar
        password_bytes = raw.encode("utf-8")[:72]
        # Recodificar de volta para string de forma segura
        safe_password = password_bytes.decode("utf-8", errors="ignore")
        return cls._context.hash(safe_password)

    @classmethod
    def verify_password(cls, raw: str, hashed: str) -> bool:
        """Verify a password against a hash"""
        # Bcrypt tem limite de 72 bytes - truncar antes de processar
        password_bytes = raw.encode("utf-8")[:72]
        # Recodificar de volta para string de forma segura
        safe_password = password_bytes.decode("utf-8", errors="ignore")
        return cls._context.verify(safe_password, hashed)
