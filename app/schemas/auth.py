# auth pydantic schemas
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional


class AuthJWTResponse(BaseModel):
    access_token: str
    created_at: datetime = datetime.now(timezone.utc)


class AuthJWTData(BaseModel):
    name: str
    active: bool = False
    role: Optional[str] = "user"
    profile_picture_url: Optional[str] = None
