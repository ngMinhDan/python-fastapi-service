# User API router
from fastapi import APIRouter
from app.schemas.user import UserRegisterRequest

router = APIRouter()

@router.post("/users/register")
def user_register(request: UserRegisterRequest):
    return {"user": "minhdan"}
