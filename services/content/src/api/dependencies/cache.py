from typing import Annotated

from cache import Cache
from cache_storage import CacheStorage
from fastapi import Depends, Request


def get_storage(request: Request) -> CacheStorage:
    return request.app.state.cache_storage


def get_cache(
    storage: Annotated[CacheStorage, Depends(get_storage)],
) -> Cache:
    return Cache(storage=storage)
