from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from .schemas import (
        ServiceGenreFilters,
        ServiceGenreModel,
    )


class GenreServiceABC(ABC):
    """Контракт сервисного слоя для работы с жанрами"""

    @abstractmethod
    async def get_genres(
        self,
        filters: "ServiceGenreFilters",
    ) -> list["ServiceGenreModel"]:
        """Получить список жанров"""

    @abstractmethod
    async def get_genre_by_uuid(
        self,
        person_id: UUID,
    ) -> "ServiceGenreModel | None":
        """Получить детальную информацию о жанре по идентификатору"""
