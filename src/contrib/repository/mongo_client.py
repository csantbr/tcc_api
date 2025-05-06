from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from pydantic.networks import MultiHostDsn


class MongoDsn(MultiHostDsn):
    allowed_schemes = {'mongodb'}

    __slots__ = ()


class Config(BaseModel):
    host: MongoDsn
    max_pool_size: int
    min_pool_size: int
    tz_aware: bool
    connect: bool
    uuid_representation: str
    server_selection_timeout_ms: float = Field(default=30000)
    timeout_ms: float = Field(default=3000)


class MongoClient:
    _client: AsyncIOMotorClient = None

    async def get(self: 'MongoClient') -> AsyncIOMotorClient:
        return self._client

    async def connect(self: 'MongoClient', config: Config) -> None:
        self._client = AsyncIOMotorClient(
            host=config.host,
            maxPoolSize=config.max_pool_size,
            minPoolSize=config.min_pool_size,
            tz_aware=config.tz_aware,
            connect=config.connect,
            uuidRepresentation=config.uuid_representation,
            serverSelectionTimeoutMS=config.server_selection_timeout_ms,
            timeoutMS=config.timeout_ms,
        )

    async def close(self: 'MongoClient') -> None:
        self._client.close()
