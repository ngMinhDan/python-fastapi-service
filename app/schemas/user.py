# Pydantic schemas request/response
from pydantic import BaseModel
from datetime import datetime


class UserRegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class UserRegisterResponse(BaseModel):
    id: int
    name: str
    email: str
    updated_at: datetime
    created_at: datetime


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserLoginResponse(BaseModel):
    id: int
    name: str
    email: str
    updated_at: datetime
    created_at: datetime
