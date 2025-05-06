from motor.motor_asyncio import AsyncIOMotorClient

from src.config import settings
from src.contrib.repository.mongodb import db


async def connect_to_mongo() -> None:
    db.client = AsyncIOMotorClient(
        settings.MONGODB_URL,
        maxPoolSize=settings.MONGODB_MAX_CONNECTIONS_COUNT,
        minPoolSize=settings.MONGODB_MIN_CONNECTIONS_COUNT,
        tz_aware=True,
        connect=True,
        uuidRepresentation='standard',
    )


async def close_mongo_connection() -> None:
    db.client.close()
