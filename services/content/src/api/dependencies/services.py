from typing import Annotated

from cache import Cache
from core.database import FilmRepository, GenreRepository, PersonRepository
from core.services import (
    FilmServiceABC,
    GenreServiceABC,
    PersonServiceABC,
)
from fastapi import Depends
from services import FilmService, GenreService, PersonService

from api.dependencies import get_cache, get_elastic_search_database


def get_film_service(
    elastic_search_database: Annotated[
        FilmRepository,
        Depends(get_elastic_search_database),
    ],
    cache: Annotated[Cache, Depends(get_cache)],
) -> FilmServiceABC:
    return FilmService(
        elastic_search_database=elastic_search_database,
        cache=cache,
    )


def get_person_service(
    elastic_search_database: Annotated[
        PersonRepository,
        Depends(get_elastic_search_database),
    ],
    cache: Annotated[Cache, Depends(get_cache)],
) -> PersonServiceABC:
    return PersonService(
        elastic_search_database=elastic_search_database,
        cache=cache,
    )


def get_genre_service(
    elastic_search_database: Annotated[
        GenreRepository,
        Depends(get_elastic_search_database),
    ],
    cache: Annotated[Cache, Depends(get_cache)],
) -> GenreServiceABC:
    return GenreService(
        elastic_search_database=elastic_search_database,
        cache=cache,
    )
