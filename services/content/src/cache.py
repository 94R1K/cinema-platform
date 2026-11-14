import hashlib
import json
import logging
from collections.abc import Awaitable, Callable
from typing import Any, ParamSpec, TypeVar

from cache_storage import CacheStorage
from pydantic import BaseModel, TypeAdapter, ValidationError


P = ParamSpec("P")
T = TypeVar("T")

logger = logging.getLogger(__name__)


class Cache:
    def __init__(
        self,
        storage: CacheStorage,
        prefix: str = "cache",
    ) -> None:
        self._storage = storage
        self._prefix = prefix

    async def call(
        self,
        func: Callable[P, Awaitable[T]],
        result_type: Any,
        timeout_seconds: int = 60,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        key = self._generate_key(
            func,
            *args,
            **kwargs,
        )

        cached = await self._storage.get(key)

        if isinstance(cached, str):
            try:
                return self._deserialize(
                    cached,
                    result_type,
                )
            except (json.JSONDecodeError, ValidationError):
                logger.warning("Cache miss due to invalid data for key=%s", key)

        result = await func(*args, **kwargs)

        await self._storage.set(
            key,
            self._serialize(result),
            ex=timeout_seconds,
        )

        return result

    def _generate_key(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> str:
        key_data = {
            "module": func.__module__,
            "qualname": func.__qualname__,
            "args": self._serialize_for_key(args),
            "kwargs": self._serialize_for_key(kwargs),
        }

        serialized = json.dumps(
            key_data,
            sort_keys=True,
            ensure_ascii=False,
            default=str,
        )

        key_hash = hashlib.sha256(
            serialized.encode(),
        ).hexdigest()

        return f"{self._prefix}:{key_hash}"

    def _serialize_for_key(self, value: Any) -> Any:
        if isinstance(value, BaseModel):
            return value.model_dump(
                mode="json",
            )

        if isinstance(value, dict):
            return {
                str(key): self._serialize_for_key(item)
                for key, item in value.items()
            }

        if isinstance(value, (list, tuple)):
            return [
                self._serialize_for_key(item)
                for item in value
            ]

        if isinstance(value, set):
            return sorted(
                self._serialize_for_key(item)
                for item in value
            )

        return value

    @staticmethod
    def _serialize(value: Any) -> str:
        if isinstance(value, BaseModel):
            value = value.model_dump(
                mode="json",
            )

        elif isinstance(value, list):
            value = [
                item.model_dump(mode="json")
                if isinstance(item, BaseModel)
                else item
                for item in value
            ]

        return json.dumps(
            value,
            ensure_ascii=False,
        )

    @staticmethod
    def _deserialize(
        value: str,
        result_type: Any,
    ) -> Any:
        data = json.loads(value)

        return TypeAdapter(result_type).validate_python(data)
