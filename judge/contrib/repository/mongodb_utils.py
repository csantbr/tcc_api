import logging
from motor.motor_asyncio import AsyncIOMotorClient

from judge.config import settings
from judge.contrib.repository.mongodb import db

logger = logging.getLogger(__name__)


async def connect_to_mongo() -> None:
    try:
        logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL}")
        db.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            maxPoolSize=settings.MONGODB_MAX_CONNECTIONS_COUNT,
            minPoolSize=settings.MONGODB_MIN_CONNECTIONS_COUNT,
            tz_aware=True,
            connect=True,
            uuidRepresentation='standard',
        )
        await db.client.admin.command('ping')
        logger.info("MongoDB connection established successfully")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise


async def close_mongo_connection() -> None:
    if db.client:
        logger.info("Closing MongoDB connection")
        db.client.close()
        db.client = None
