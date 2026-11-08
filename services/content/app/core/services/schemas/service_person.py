from uuid import UUID

from pydantic import BaseModel


class ServicePersonFilms(BaseModel):
    uuid: UUID
    roles: list[str]


class ServicePersonModel(BaseModel):
    """Модель персоны."""

    uuid: UUID
    full_name: str


class ServicePersonModelWithFilms(ServicePersonModel):
    """Модель персоны с фильмами."""

    films: list[ServicePersonFilms]
