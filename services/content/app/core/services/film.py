from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from .schemas import (
        ServiceFilmFilters,
        ServiceFilmFullModel,
        ServiceFilmModel,
        ServiceFilmSearchFilters,
    )


class FilmServiceABC(ABC):
    """Контракт сервисного слоя для работы с фильмами."""

    @abstractmethod
    async def get_films(
        self,
        filters: "ServiceFilmFilters",
    ) -> list["ServiceFilmModel"]:
        """Получить список фильмов по заданным параметрам."""

    @abstractmethod
    async def search_films(
        self,
        filters: "ServiceFilmSearchFilters",
    ) -> list["ServiceFilmModel"]:
        """Найти фильмы по поисковому запросу."""

    @abstractmethod
    async def get_film_by_id(
        self,
        film_id: UUID,
    ) -> "ServiceFilmFullModel | None":
        """Получить детальную информацию о фильме по идентификатору."""
