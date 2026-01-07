from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from src.core.config import settings
from fastapi import HTTPException, status

class AccessToken:
    @staticmethod
    def generate(user_id: str, role: str, remember: bool) -> str:
        if remember:
            expire_time = timedelta(days=7)
        else:
            expire_time = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        
        expire = datetime.now(timezone.utc) + expire_time
        
        payload = {
            "sub": str(user_id), 
            "role": role,        
            "exp": expire,
            "iat": datetime.now(timezone.utc)
        }

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    @staticmethod
    def decode(token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return payload
        
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )