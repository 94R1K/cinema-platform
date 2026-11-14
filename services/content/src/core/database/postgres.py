from abc import ABC, abstractmethod
from typing import Any


class PostgresDatabaseABC(ABC):
    @abstractmethod
    async def get_films() -> list[Any]:
        ...

    @abstractmethod
    async def get_persons() -> list[Any]:
        ...

    @abstractmethod
    async def get_genres() -> list[Any]:
        ...
