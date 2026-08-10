from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config import settings

_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongo.connection_uri)
    return _client


def get_database() -> AsyncIOMotorDatabase:
    return get_client().get_database(settings.mongo.database_name)


async def close_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None

