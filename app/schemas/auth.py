# auth pydantic schemas
from pydantic import BaseModel
from datetime import datetime

class AuthJWTResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    created_at: datetime