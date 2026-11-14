import pytest_asyncio
from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from tests.core.settings import settings

from .utils import prepare_data
from .utils.wait_for_dependencies import (
    wait_for_api_ready,
    wait_for_elasticsearch_ready,
    wait_for_redis_ready,
)


INDEXES = [
    settings.es_movies_index_name,
    settings.es_persons_index_name,
    settings.es_genre_index_name,
]


@pytest_asyncio.fixture(
    scope="session",
    loop_scope="session",
    autouse=True
)
async def prepare_elasticsearch(es_client):

    await es_client.cluster.health(
        wait_for_status="yellow",
        timeout="60s",
    )

    for index_name in INDEXES:
        await prepare_data(
            es=es_client,
            es_index_name=index_name,
        )

    yield


@pytest_asyncio.fixture(
    scope="session",
    loop_scope="session",
)
async def client_session():
    async with ClientSession() as session:
        yield session


@pytest_asyncio.fixture(
    scope="session",
    loop_scope="session",
)
async def es_client():
    async with AsyncElasticsearch(
        hosts=[settings.elasticsearch_url, ],
        verify_certs=False,
    ) as client:
        yield client


@pytest_asyncio.fixture(
    scope="session",
    loop_scope="session",
)
async def redis_client():
    async with Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        decode_responses=True,
    ) as client:
        yield client


@pytest_asyncio.fixture(
    scope="session",
    autouse=True,
)
async def api_ready(client_session: ClientSession):
    await wait_for_api_ready(
        session=client_session,
        url=f"{settings.service_url}/api/v1/health",
    )


@pytest_asyncio.fixture(
    scope="session",
    autouse=True,
)
async def elasticsearch_ready(es_client: AsyncElasticsearch):
    await wait_for_elasticsearch_ready(
        es_client=es_client,
    )


@pytest_asyncio.fixture(
    scope="session",
    autouse=True,
)
async def redis_ready(redis_client: Redis):
    await wait_for_redis_ready(
        redis_client=redis_client,
    )
