from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.ratelimit import SlidingWindowRateLimit, FixedWindowRateLimit
from app.core.config import config


def setup_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_config.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SlidingWindowRateLimit)
