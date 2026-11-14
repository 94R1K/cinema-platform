import abc
import json
from typing import Any

from database.redis.client import RedisClient


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния."""

    @abc.abstractmethod
    def save_state(self, state: dict[str, Any]) -> None:
        """Сохранить состояние."""

    @abc.abstractmethod
    def retrieve_state(self) -> dict[str, Any]:
        """Получить состояние."""


class RedisStorage(BaseStorage):
    def __init__(
        self,
        redis: RedisClient,
        key: str = "etl:state",
    ) -> None:
        self.redis = redis.connection
        self.key = key

    def save_state(self, state: dict[str, Any]) -> None:
        mapping = {
            key: json.dumps(value)
            for key, value in state.items()
        }

        if mapping:
            self.redis.hset(self.key, mapping=mapping)

    def retrieve_state(self) -> dict[str, Any]:
        state = self.redis.hgetall(self.key)

        return {
            key.decode() if isinstance(key, bytes) else key: json.loads(value)
            for key, value in state.items()
        }
