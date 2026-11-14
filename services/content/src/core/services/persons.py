from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from uuid import UUID


if TYPE_CHECKING:
    from .schemas import (
        ServicePersonFilms,
        ServicePersonFilters,
        ServicePersonModelWithFilms,
    )


class PersonServiceABC(ABC):
    """Контракт сервисного слоя для работы с персонами"""

    @abstractmethod
    async def get_persons(
        self,
        filters: ServicePersonFilters,
    ) -> list[ServicePersonModelWithFilms]:
        """Получить список персон по заданным параметрам"""

    @abstractmethod
    async def get_person_films_by_uuid(
        self,
        person_id: UUID,
    ) -> list[ServicePersonFilms]:
        """Получить список фильмов по идентификатору персоны"""

    @abstractmethod
    async def get_person_by_uuid(
        self,
        person_id: UUID,
    ) -> ServicePersonModelWithFilms | None:
        """Получить детальную информацию о персоне по идентификатору"""
