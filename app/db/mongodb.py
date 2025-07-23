from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user import User


class MongoClient:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "test"):
        self.uri = uri
        self.client = AsyncIOMotorClient(host=self.uri, maxPoolSize=100, minPoolSize=1)
        self.db_name = db_name

    async def connect_mongodb(self):
        await init_beanie(database=self.client[self.db_name], document_models=[User])

    async def close_mongodb(self):
        await self.client.close()
