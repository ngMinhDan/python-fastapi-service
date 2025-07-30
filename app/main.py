# Fast API app instance & startup logic
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.mongodb import MongoClient
from app.api import router as router
from app.core.middleware import setup_middleware

mongo_client = MongoClient()


# lifespan for fastapi app , new and modern way to manage startup and shutdown logic
@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_client.connect_mongodb()
    yield
    await mongo_client.close_mongodb()


def create_app():
    app = FastAPI(
        title="FastAPI Server",
        description="FastAPI Server",
        version="0.0.1",
        lifespan=lifespan,
    )
    setup_middleware(app)
    app.include_router(router, prefix="")
    return app
