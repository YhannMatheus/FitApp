from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from src.core.config import settings
from fastapi import HTTPException, status
from src.types.schemas.auth import TokenData
from src.types.enums.user import RoleEnum

class AccessToken:
    @staticmethod
    def generate(user_id: str, role: str, remember: bool = False) -> str:
        if remember:
            expire_time = timedelta(days=settings.JWT_EXPIRE_DAYS_REMEMBER)
        else:
            expire_time = timedelta(days=settings.JWT_EXPIRE_DAYS)
        
        expire = datetime.now(timezone.utc) + expire_time
        
        payload = {
            "sub": user_id,
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
    def decode(token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )

            user_id = payload.get("sub")
            email = payload.get("email")
            role_str = payload.get("role")
            
            if user_id is None or role_str is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Converter string para RoleEnum
            try:
                role = RoleEnum(role_str)
            except (ValueError, KeyError):
                role = RoleEnum.USER
            
            token_data = TokenData(
                user_id=user_id,
                email=email,
                role=role,
            )
            return token_data
        
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )