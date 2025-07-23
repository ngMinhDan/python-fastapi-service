from fastapi import APIRouter
from app.api.v1.user import router as user_router
from app.api.health import router as health_router

router = APIRouter()
router.include_router(user_router, prefix="/api/v1")
router.include_router(health_router, prefix="")
