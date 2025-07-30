# load config from config/settings.toml

import toml
from pydantic import BaseModel


class MongoConfig(BaseModel):
    MONGODB_URL: str
    MONGODB_DATABASE: str


class JWTConfig(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int


class CORSConfig(BaseModel):
    ORIGINS: list[str]


class RateLimitConfig(BaseModel):
    MAX_REQUESTS: int
    WINDOW_SEC: int


class Config(BaseModel):
    mongodb_config: MongoConfig
    jwt_config: JWTConfig
    cors_config: CORSConfig
    rate_limit_config: RateLimitConfig


with open("config/settings.toml", "r") as f:
    config = toml.load(f)
    config = Config(**config)
