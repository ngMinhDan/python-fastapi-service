from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated

import jwt

from fastapi import Depends, FastAPI, HTTPException, status, Header
from pydantic import BaseModel

from app.schemas.auth import AuthJWTData, AuthJWTResponse
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.core.config import config

SECRET_KEY = config.jwt_config.SECRET_KEY
ALGORITHM = config.jwt_config.ALGORITHM
EXPIRE_MINUTES = config.jwt_config.EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # get token from header


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # no change the data dict
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
