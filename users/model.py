from typing import Optional
from sqlmodel import Field, Session, SQLModel, select
from datetime import datetime, timezone


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    hashed_password: str
    created: datetime | None = Field(default=datetime.now(timezone.utc))
    updated: datetime | None

    @classmethod
    def find_by_email(cls, session: Session, email: str) -> Optional["User"]:
        statement = select(cls).where(cls.email == email)
        return session.exec(statement).first()
