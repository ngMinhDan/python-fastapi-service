# Fast API app instance & startup logic
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.mongodb import MongoClient
from app.api import router as router
from app.core.ratelimit import SlidingWindowRateLimit


mongo_client = MongoClient()


# lifespan for fastapi app , new and modern way to manage startup and shutdown logic
@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_client.connect_mongodb()
    yield
    await mongo_client.close_mongodb()


app = FastAPI(
    title="FastAPI Server",
    description="FastAPI Server",
    version="0.0.1",
    lifespan=lifespan,
)

app.add_middleware(SlidingWindowRateLimit)
app.include_router(router, prefix="")
