# User API router
from fastapi import APIRouter
from app.schemas.user import UserRegisterRequest, UserLoginRequest

router = APIRouter()

@router.post("/users/register")
def user_register(request: UserRegisterRequest):
    return {"user": "minhdan"}

@router.post("/users/login")
def user_login(request: UserLoginRequest):
    return {"user": "minhdan"}
