from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SessionBase(BaseModel):
    user_id: str
    created_at: datetime
    expires_at: datetime