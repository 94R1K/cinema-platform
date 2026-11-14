from typing import TYPE_CHECKING
from uuid import UUID

from core.database.schemas import ElasticSearchGenreModel
from core.services import GenreServiceABC
from core.services.schemas import ServiceGenreModel


if TYPE_CHECKING:
    from cache import Cache
    from core.database import ElasticSearchDatabaseABC
    from core.services.schemas import ServiceGenreFilters


class GenreService(GenreServiceABC):
    """Сервисный слой для работы с жанрами"""

    def __init__(
        self,
        elastic_search_database: ElasticSearchDatabaseABC,
        cache: Cache,
    ) -> None:
        self._database = elastic_search_database
        self._cache = cache

    async def get_genres(
        self,
        filters: ServiceGenreFilters,
    ) -> list[ServiceGenreModel]:
        genres_from_db = await self._cache.call(
            func = self._database.get_genres,
            result_type=list[ElasticSearchGenreModel],
            filters=filters.to_elasticsearch_filters(),
        )

        return [
            ServiceGenreModel(
                uuid=genre.id,
                name=genre.name,
            )
            for genre in genres_from_db
        ]

    async def get_genre_by_uuid(
        self,
        genre_uuid: UUID,
    ) -> ServiceGenreModel | None:
        if not (genre := await self._database.get_genre_by_uuid(genre_uuid)):
            return None

        return ServiceGenreModel(
            uuid=genre.id,
            name=genre.name,
        )
