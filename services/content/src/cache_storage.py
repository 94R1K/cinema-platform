import logging
from abc import ABC, abstractmethod

from redis import RedisError
from redis.asyncio import Redis


logger = logging.getLogger(__name__)

class CacheStorage(ABC):
    @abstractmethod
    async def get(self, key: str) -> str | None:
        """Получить значение по ключу"""

    @abstractmethod
    async def set(self, key: str, value: str, ex: int = 3600) -> None:
        """Положить значение по ключу"""


class RedisStorage(CacheStorage):
    def __init__(self, client: Redis):
        self.client = client

    async def get(self, key: str) -> str | None:
        try:
            return await self.client.get(key)
        except RedisError:
            logger.warning(
                "Redis cache read failed. "
                "Calling the original function. "
                "Cache key: %s",
                key,
                exc_info=True,
            )

    async def set(self, key: str, value: str, ex: int | None = None) -> None:
        try:
            await self.client.set(key, value, ex=ex)
        except RedisError:
            logger.warning(
                "Redis cache write failed. "
                "Returning the original result. "
                "Cache key: %s",
                key,
                exc_info=True,
            )
