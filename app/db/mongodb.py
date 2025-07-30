from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user import User
from app.core.config import config


class MongoClient:
    def __init__(self):
        self.uri = config.mongodb_config.MONGODB_URL
        self.client = AsyncIOMotorClient(host=self.uri, maxPoolSize=100, minPoolSize=1)
        self.db_name = config.mongodb_config.MONGODB_DATABASE

    async def connect_mongodb(self):
        await init_beanie(database=self.client[self.db_name], document_models=[User])

    async def close_mongodb(self):
        self.client.close()
