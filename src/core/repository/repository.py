from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from src.config import settings


class Repository:
    def __init__(self, db: AsyncIOMotorClient):
        self.db: AsyncIOMotorClient = db
        self.collection: AsyncIOMotorCollection = self.db[settings.MONGODB_DATABASE][settings.MONGODB_COLLECTION]
