from motor.motor_asyncio import AsyncIOMotorClient

from src.core.db import db
from src.core.repository import FormRepo


async def get_database() -> AsyncIOMotorClient:
    """
    Get a MongoDB database instance.

    :return: AsyncIOMotorClient - MongoDB database instance.
    """
    return db.client


async def form_repo() -> FormRepo:
    """
    Dependency Injection for the FormRepo repository.

    :return: FormRepo - FormRepo repository instance.
    """
    db = await get_database()
    return FormRepo(db)
