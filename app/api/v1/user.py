# User API router
from fastapi import APIRouter
from app.schemas.user import UserRegisterRequest
from app.schemas.auth import AuthJWTResponse
from app.core.security import create_access_token, get_password_hash
from app.models.user import User
from fastapi import HTTPException
import re

router = APIRouter()


@router.post("/users/register")
async def user_register(request: UserRegisterRequest):
    if not re.match("^[^@]+@[^@]+\.[^@]+", request.email):
        raise HTTPException(status_code=400, detail="Invalid email")

    if len(request.password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters long"
        )

    is_exists = await User.find_emails(request.email)
    if is_exists:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        name=request.name,
        email=request.email,
        hashed_password=get_password_hash(request.password),
    )
    await user.save()

    data_payload = {
        "name": request.name,
        "active": False,
        "profile_picture_url": None,
        "cover_picture_url": None,
    }
    access_token = create_access_token(data=data_payload)
    return AuthJWTResponse(access_token=access_token)
