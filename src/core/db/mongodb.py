import json
import logging
import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from src.config import settings
from src.utils import get_logger

logger = get_logger(log_level=logging.DEBUG)


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def connect_to_mongo() -> None:
    """
    Connect to MongoDB using the AsyncIOMotorClient.

    Returns:
        None
    """
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)


async def close_mongo_connection() -> None:
    """
    Close the MongoDB connection.

    Returns:
        None
    """
    db.client.close()


async def check_database() -> None:
    """
    Check if the MongoDB database is empty and initialize it if needed.

    Returns:
        None
    """
    collection = db.client[settings.MONGODB_DATABASE][settings.MONGODB_COLLECTION]
    data = await collection.find_one()
    if data:
        logger.info(f"The database is not empty. Skipping initialization.")
    else:
        logger.info("The database is empty.")
        logger.info("Database initialization is in progress...")
        await initialize_database(collection=collection)


async def initialize_database(collection: AsyncIOMotorCollection) -> None:
    """
    Initialize the MongoDB database by inserting data from initial_data.json.

    Args:
        collection (AsyncIOMotorCollection): The MongoDB collection to insert data into.

    Returns:
        None
    """
    path = os.path.dirname(__file__)
    file_path = os.path.join(path, "initial_data.json")
    try:
        with open(file_path, "r") as file:
            initial_data = json.load(file)
        await collection.insert_many(initial_data)
    except FileNotFoundError:
        logger.error("Error: initial_data.json not found!")
    except Exception as e:
        logger.error(f"Error during database initialization! Detail: {e}")
    else:
        logger.info("Initialization completed.")
