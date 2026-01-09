from fastapi import HTTPException, status
from src.types.models.session import Session
from src.types.schemas.session import SessionBase
from datetime import datetime, timezone, timedelta
from uuid import UUID

class SessionService:
    @staticmethod
    async def create_session(user_id: str, remember: bool) -> SessionBase:
        """Create a new session for the user with an expiration time based on the 'remember' flag."""
        if remember:
            expire_time = timedelta(days=7)
        else:
            expire_time = timedelta(days=1)

        expires_at = datetime.now(timezone.utc) + expire_time

        # Converter user_id de string para UUID
        user_uuid = UUID(user_id)

        # Buscar sessão existente do usuário
        existing_session = await Session.filter(user_id=user_uuid).first()

        if existing_session:
            # Atualizar sessão existente
            existing_session.expires_at = expires_at
            await existing_session.save()
            return SessionBase(
                user_id=user_id,
                created_at=existing_session.created_at,
                expires_at=existing_session.expires_at
            )
        
        # Criar nova sessão
        new_session = await Session.create(
            user_id=user_uuid,
            expires_at=expires_at
        )
        return SessionBase(
            user_id=user_id,
            created_at=new_session.created_at,
            expires_at=new_session.expires_at
        )
        
    @staticmethod
    async def get_session(userId: str) -> SessionBase:
        # Converter userId de string para UUID
        user_uuid = UUID(userId)
        
        session = await Session.filter(user_id=user_uuid).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
            )
        
        if session.expires_at < datetime.now(timezone.utc):
            await session.delete()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Session has expired"
            )
        elif session.expires_at >= datetime.now(timezone.utc):
            session.expires_at = datetime.now(timezone.utc) + timedelta(days=7)
            await session.save()

        return SessionBase(
            user_id=userId,
            created_at=session.created_at,
            expires_at=session.expires_at
        )