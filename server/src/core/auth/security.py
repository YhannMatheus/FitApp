from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from src.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    from src.services.user_services import UserService

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception
    user = await UserService.get_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user


class Password:
    _context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, raw: str) -> str:
        # Bcrypt tem limite de 72 bytes - truncar antes de processar
        password_bytes = raw.encode("utf-8")[:72]
        # Recodificar de volta para string de forma segura
        safe_password = password_bytes.decode("utf-8", errors="ignore")
        return cls._context.hash(safe_password)

    @classmethod
    def verify(cls, raw: str, hashed: str) -> bool:
        # Bcrypt tem limite de 72 bytes - truncar antes de processar
        password_bytes = raw.encode("utf-8")[:72]
        # Recodificar de volta para string de forma segura
        safe_password = password_bytes.decode("utf-8", errors="ignore")
        return cls._context.verify(safe_password, hashed)
