from datetime import datetime, timedelta
from jose import jwt
from src.core.config import settings


class AccessToken:
    def __init__(self, subject: str):
        self.subject = subject

    def generate(self) -> str:
        payload = {
            "sub": self.subject,
            "exp": datetime.utcnow()
            + timedelta(minutes=settings.JWT_EXPIRE_MINUTES),
        }

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
