# Fast API app instance & startup logic
from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.v1.user import router as user_router

app = FastAPI(title="FastAPI Server", description="FastAPI Server", version="0.0.1")

app.include_router(health_router, prefix="")
app.include_router(user_router, prefix="/api/v1")
