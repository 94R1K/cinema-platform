from typing import TYPE_CHECKING
from uuid import UUID

import backoff
from core.database import FilmRepository, GenreRepository, PersonRepository
from core.database.schemas import (
    ELasticSearchFilmFullModel,
    ELasticSearchFilmModel,
    ElasticSearchFilmSearchFilter,
    ElasticSearchFilter,
    ElasticSearchGenreFilter,
    ElasticSearchGenreModel,
    ElasticSearchPersonFilmsModel,
    ElasticSearchPersonFilter,
    ElasticSearchPersonModel,
)
from elastic_transport import (
    ConnectionError as ElasticConnectionError,
    ConnectionTimeout,
)
from elasticsearch import NotFoundError


if TYPE_CHECKING:
    from core.database.schemas import ElasticSearchFilmFilter
    from elasticsearch import AsyncElasticsearch


class ElasticSearchDatabase(FilmRepository, GenreRepository, PersonRepository):
    """Класс БД для работы с ElasticSearch."""

    def __init__(self, elastic_search_client: AsyncElasticsearch) -> None:
        self._client = elastic_search_client

    @backoff.on_exception(
        backoff.expo,
        (ElasticConnectionError, ConnectionTimeout),
        max_tries=3,
        jitter=backoff.full_jitter,
    )
    async def _search(self, **kwargs):
        return await self._client.search(**kwargs)

    @backoff.on_exception(
        backoff.expo,
        (ElasticConnectionError, ConnectionTimeout),
        max_tries=3,
        jitter=backoff.full_jitter,
    )
    async def _get(self, **kwargs):
        return await self._client.get(**kwargs)

    def _buid_filter(self, index: str, filters: ElasticSearchFilter) -> dict[str, str]:
        query: dict = {
            "bool": {
                "filter": [],
            },
        }

        search_kwargs: dict = {
            "index": index,
            "query": query,
            "from_": (filters.page_number - 1) * filters.page_size,
            "size": filters.page_size,
        }

        if filters.sort_by:
            search_kwargs["sort"] = [
                {
                    filters.sort_by: {
                        "order": filters.sort_direction or "asc",
                    },
                },
            ]

        return search_kwargs

    async def get_films(
        self,
        filters: ElasticSearchFilmFilter,
    ) -> list[ELasticSearchFilmModel]:
        search_kwargs = self._buid_filter("movies", filters)

        if filters.genre_id:
            search_kwargs["query"]["bool"]["filter"].append(
                {
                    "nested": {
                        "path": "genres",
                        "query": {
                            "term": {
                                "genres.id": str(filters.genre_id),
                            },
                        },
                    },
                },
            )

        response = await self._search(**search_kwargs)

        return [
            ELasticSearchFilmModel(
                **hit["_source"],
            )
            for hit in response["hits"]["hits"]
        ]

    async def search_films(
        self,
        filters: ElasticSearchFilmSearchFilter,
    ) -> list[ELasticSearchFilmModel]:
        query = {
            "multi_match": {
                "query": filters.query,
                "fields": [
                    "title",
                    "description",
                    "actors_names",
                    "writers_names",
                    "directors_names",
                ],
            },
        }

        search_kwargs: dict = {
            "index": "movies",
            "query": query,
            "from_": (filters.page_number - 1) * filters.page_size,
            "size": filters.page_size,
        }

        response = await self._search(**search_kwargs)

        return [
            ELasticSearchFilmModel(
                **hit["_source"],
            )
            for hit in response["hits"]["hits"]
        ]

    async def get_film_by_id(
        self,
        film_id: UUID,
    ) -> ELasticSearchFilmFullModel | None:
        try:
            response = await self._get(
                index="movies",
                id=str(film_id),
            )
        except NotFoundError:
            return None

        return ELasticSearchFilmFullModel(**response["_source"])

    async def get_persons(self, filters: ElasticSearchPersonFilter):
        search_kwargs = self._buid_filter("persons", filters)

        if filters.full_name:
            search_kwargs["query"]["bool"]["filter"].append(
                {"match_phrase": {"full_name": filters.full_name}}
            )

        response = await self._search(**search_kwargs)

        return [
            ElasticSearchPersonModel(
                **hit["_source"],
            )
            for hit in response["hits"]["hits"]
        ]

    async def get_person_by_uuid(self, person_uuid):
        try:
            response = await self._get(
                index="persons",
                id=str(person_uuid),
            )
        except NotFoundError:
            return None

        return ElasticSearchPersonModel(**response["_source"])

    async def get_person_film_by_uuid(
        self, person_uuid: UUID
    ) -> list[ElasticSearchPersonFilmsModel]:
        try:
            person = await self._get(
                index="persons",
                id=str(person_uuid),
            )

            film_uuids = [film["id"] for film in person["_source"]["films"]]
            response = await self._search(
                index="movies",
                body={
                    "query": {"ids": {"values": film_uuids}},
                },
            )

        except NotFoundError:
            return None

        return [
            ELasticSearchFilmModel(
                **hit["_source"],
            )
            for hit in response["hits"]["hits"]
        ]

    async def get_genres(
        self, filters: ElasticSearchGenreFilter
    ) -> list[ElasticSearchGenreModel]:
        search_kwargs = self._buid_filter("genres", filters)
        if filters.name:
            search_kwargs["query"]["bool"]["filter"].append(
                {
                    "prefix": {
                        "name.raw": filters.name,
                    }
                }
            )
        response = await self._search(**search_kwargs)

        return [
            ElasticSearchGenreModel(
                **hit["_source"],
            )
            for hit in response["hits"]["hits"]
        ]

    async def get_genre_by_uuid(self, genre_uuid: UUID) -> ElasticSearchGenreModel:
        try:
            response = await self._get(
                index="genres",
                id=str(genre_uuid),
            )
        except NotFoundError:
            return None

        return ElasticSearchGenreModel(**response["_source"])
