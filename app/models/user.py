from typing import Optional
from beanie import Document
from datetime import datetime, timezone


class User(Document):
    name: str
    email: str
    password: str
    hashed_password: str
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime
    active: bool = False
    role: Optional[str] = "user"
    phone: Optional[str] = None
    address: Optional[str] = None
    profile_picture_url: Optional[str] = None
    cover_picture_url: Optional[str] = None

    # overwrite save method to update updated_at field
    async def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        return await super().save(*args, **kwargs)
