from typing import TYPE_CHECKING
from uuid import UUID

from core.database.schemas import ElasticSearchPersonModel
from core.services import PersonServiceABC
from core.services.mappers.persons import service_person_model_from_elastic_search
from core.services.schemas import (
    ServiceFilmModel,
    ServicePersonModelWithFilms,
)


if TYPE_CHECKING:
    from cache import Cache
    from core.database import PersonRepository
    from core.services.schemas import ServicePersonFilters


class PersonService(PersonServiceABC):
    """Сервисный слой для работы с персонами"""

    def __init__(
        self,
        elastic_search_database: PersonRepository,
        cache: Cache,
    ) -> None:
        self._database = elastic_search_database
        self._cache = cache

    async def get_persons(
        self,
        filters: ServicePersonFilters,
    ) -> list[ServicePersonModelWithFilms]:
        persons_from_db = await self._cache.call(
            func=self._database.get_persons,
            result_type=list[ElasticSearchPersonModel],
            filters=filters.to_elasticsearch_filters(),
        )

        return [
            service_person_model_from_elastic_search(person)
            for person in persons_from_db
        ]

    async def get_person_films_by_uuid(
        self,
        person_uuid: UUID,
    ) -> list[ServiceFilmModel] | None:
        if films := await self._database.get_person_film_by_uuid(person_uuid):
            return [
                ServiceFilmModel(
                    uuid=film.id,
                    title=film.title,
                    imdb_rating=film.imdb_rating,
                )
                for film in films
            ]

        return None

    async def get_person_by_uuid(
        self,
        person_uuid: UUID,
    ) -> ServicePersonModelWithFilms | None:
        if not (person := await self._database.get_person_by_uuid(person_uuid)):
            return None

        return service_person_model_from_elastic_search(person)
