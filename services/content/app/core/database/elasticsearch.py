from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from core.database.schemas import (
        ElasticSearchFilmFilter,
        ELasticSearchFilmFullModel,
        ELasticSearchFilmModel,
        ElasticSearchFilmSearchFilter,
        ElasticSearchFilter,
        ElasticSearchGenreFilter,
        ElasticSearchGenreModel,
        ElasticSearchPersonFilter,
        ElasticSearchPersonModel,
    )

class FilmRepository(ABC):
    @abstractmethod
    async def get_films(
        self, filters: "ElasticSearchFilmFilter"
    ) -> list["ELasticSearchFilmModel"]:
        """Получить список фильмов."""

    @abstractmethod
    async def search_films(
        self,
        filters: "ElasticSearchFilmSearchFilter",
    ) -> list["ELasticSearchFilmModel"]:
        """Найти фильмы по поисковому запросу."""

    @abstractmethod
    async def get_film_by_id(
        self,
        film_id: UUID,
    ) -> "ELasticSearchFilmFullModel | None":
        """Получить детальную информацию о фильме по идентификатору."""


class GenreRepository(ABC):
    @abstractmethod
    async def get_genres(self, filters: "ElasticSearchGenreFilter") -> list["ElasticSearchGenreModel"]:
        """Получить список жанров"""

    @abstractmethod
    async def get_genre_by_uuid(self, genre_uuid: UUID) -> "ElasticSearchGenreModel":
        """Получить жанр по идентификатору"""


class PersonRepository(ABC):
    @abstractmethod
    async def get_persons(self, filters: "ElasticSearchPersonFilter") -> list["ElasticSearchPersonModel"] | None:
        """Получить список персон"""

    @abstractmethod
    async def get_person_by_uuid(self, person_uuid: UUID) -> "ElasticSearchPersonModel | None":
        """Получить информацию о персоне по идентификатору"""

    @abstractmethod
    async def get_person_film_by_uuid(self, person_uuid: UUID) -> "ElasticSearchPersonModel | None":
        """Получить список фильмов по идентификатору персоны"""
