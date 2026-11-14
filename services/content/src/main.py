import logging.config
from contextlib import asynccontextmanager

from api.routers import (
    film_router,
    genre_router,
    healthcheck_router,
    person_router,
)
from core.config import settings
from core.logger import LOGGING


logging.config.dictConfig(LOGGING)
from cache_storage import RedisStorage
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from redis.asyncio import Redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    es = AsyncElasticsearch(hosts=[settings.elasticsearch_url, ])

    redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        decode_responses=True,
    )

    app.state.elasticsearch = es
    app.state.cache_storage = RedisStorage(redis)

    try:
        yield
    finally:
        await es.close()
        await redis.aclose()


tags_metadata = [
    {"name": "films", "description": "Получение информации о фильмах"},
    {"name": "genres", "description": "Получение информации о жанрах"},
    {"name": "persons", "description": "Получение информации о персонале"}
]

app = FastAPI(
    title=settings.project_name,
    description="""
        API для клиентов онлайн-кинотеатра. Предоставляет возможность поиска 
        фильмов, жанров, сценаристов, режисеров, актеров и др. персонала
    """,
    openapi_tags=tags_metadata,
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.include_router(film_router)
app.include_router(person_router)
app.include_router(genre_router)
app.include_router(healthcheck_router)
