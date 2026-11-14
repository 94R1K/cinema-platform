import logging
from asyncio import sleep
from collections.abc import Awaitable, Callable
from time import monotonic

from aiohttp import ClientError, ClientSession
from elastic_transport import (
    ConnectionError as ElasticConnectionError,
    ConnectionTimeout,
)
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis
from redis.exceptions import RedisError


logger = logging.getLogger(__name__)


async def _wait_for_ready(
    check: Callable[[], Awaitable[bool]],
    service_name: str,
    exceptions: tuple[type[Exception], ...],
    timeout: float = 60,
    interval: float = 1,
) -> None:
    deadline = monotonic() + timeout
    last_exception: Exception | None = None

    logger.info("Waiting for %s...", service_name)

    while monotonic() < deadline:
        try:
            if await check():
                logger.info("%s is ready", service_name)
                return
        except exceptions as exc:
            last_exception = exc
            logger.warning(
                "%s is not ready: %s. Retrying in %.1f seconds...",
                service_name,
                exc,
                interval,
            )

        await sleep(interval)

    if last_exception is not None:
        raise RuntimeError(
            f"{service_name} is not ready after {timeout} seconds: {last_exception}"
        ) from last_exception

    raise RuntimeError(f"{service_name} is not ready after {timeout} seconds")


async def wait_for_api_ready(
    session: ClientSession,
    url: str,
    timeout: float = 60,
    interval: float = 1,
) -> None:
    async def check() -> bool:
        async with session.get(url) as response:
            if response.status != 200:
                raise RuntimeError(f"API returned HTTP {response.status}")
            return True

    await _wait_for_ready(
        check=check,
        service_name="API",
        exceptions=(ClientError, RuntimeError),
        timeout=timeout,
        interval=interval,
    )


async def wait_for_elasticsearch_ready(
    es_client: AsyncElasticsearch,
    timeout: float = 60,
    interval: float = 1,
) -> None:
    await _wait_for_ready(
        check=es_client.ping,
        service_name="Elasticsearch",
        exceptions=(
            ElasticConnectionError,
            ConnectionTimeout,
        ),
        timeout=timeout,
        interval=interval,
    )


async def wait_for_redis_ready(
    redis_client: Redis,
    timeout: float = 60,
    interval: float = 1,
) -> None:
    async def check() -> bool:
        return await redis_client.ping()

    await _wait_for_ready(
        check=check,
        service_name="Redis",
        exceptions=(RedisError,),
        timeout=timeout,
        interval=interval,
    )
