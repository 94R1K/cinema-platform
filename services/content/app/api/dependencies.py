from functools import lru_cache
from typing import TYPE_CHECKING

from cache import Cache
from cache_storage import CacheStorage
from db import ElasticSearchDatabase
from fastapi import Depends, Request
from services import FilmService, GenreService, PersonService

from elasticsearch import AsyncElasticsearch

if TYPE_CHECKING:
    from core.database import FilmRepository, GenreRepository, PersonRepository
    from core.services import FilmServiceABC, PersonServiceABC


def get_elasticsearch(request: Request) -> AsyncElasticsearch:
    return request.app.state.elasticsearch

def get_storage(request: Request) -> CacheStorage:
    return request.app.state.cache_storage

@lru_cache
def get_elastic_search_database(
    elastic_search_client: AsyncElasticsearch = Depends(get_elasticsearch),
) -> "ElasticSearchDatabase":
    return ElasticSearchDatabase(elastic_search_client=elastic_search_client)

def get_cache(storage: CacheStorage = Depends(get_storage)) -> Cache:
    return Cache(storage=storage)

@lru_cache
def get_film_service(
    elastic_search_database: "FilmRepository" = Depends(
        get_elastic_search_database
    ),
    cache: Cache = Depends(get_cache),
) -> "FilmServiceABC":
    return FilmService(
        elastic_search_database=elastic_search_database,
        cache=cache,
    )

@lru_cache
def get_person_service(
    elastic_search_database: "GenreRepository" = Depends(get_elastic_search_database),
    cache: Cache = Depends(get_cache),
) -> "PersonServiceABC":
    return PersonService(
        elastic_search_database=elastic_search_database,
        cache=cache
    )

@lru_cache
def get_genre_service(
    elastic_search_database: "PersonRepository" = Depends(get_elastic_search_database),
    cache: Cache = Depends(get_cache),
) -> "PersonServiceABC":
    return GenreService(
        elastic_search_database=elastic_search_database,
        cache=cache
    )
