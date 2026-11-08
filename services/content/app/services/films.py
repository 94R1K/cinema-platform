from typing import TYPE_CHECKING
from uuid import UUID

from core.database.schemas import ELasticSearchFilmModel
from core.services import FilmServiceABC
from core.services.mappers import service_film_full_model_from_elastic_search
from core.services.schemas import ServiceFilmModel, ServiceFilmSearchFilters

if TYPE_CHECKING:
    from cache import Cache
    from core.database import ElasticSearchDatabaseABC
    from core.services.schemas import ServiceFilmFilters


class FilmService(FilmServiceABC):
    """Сервисный слой для работы с фильмами."""

    def __init__(
        self,
        elastic_search_database: "ElasticSearchDatabaseABC",
        cache: "Cache",
    ) -> None:
        self._database = elastic_search_database
        self._cache = cache

    async def get_films(
        self,
        filters: "ServiceFilmFilters",
    ) -> list[ServiceFilmModel]:
        films_from_db = await self._cache.call(
            func=self._database.get_films,
            result_type=list[ELasticSearchFilmModel],
            filters=filters.to_elasticsearch_filters(),
        )

        return [
            ServiceFilmModel(
                uuid=film.id,
                title=film.title,
                imdb_rating=film.imdb_rating,
            )
            for film in films_from_db
        ]

    async def search_films(
        self,
        filters: ServiceFilmSearchFilters,
    ) -> list[ServiceFilmModel]:
        films_from_db = await self._database.search_films(
            filters.to_elasticsearch_filters(),
        )

        return [
            ServiceFilmModel(
                uuid=film.id,
                title=film.title,
                imdb_rating=film.imdb_rating,
            )
            for film in films_from_db
        ]

    async def get_film_by_id(
        self,
        film_id: UUID,
    ) -> ServiceFilmModel | None:
        if not (film_from_db := await self._database.get_film_by_id(film_id)):
            return

        return service_film_full_model_from_elastic_search(film_from_db)
