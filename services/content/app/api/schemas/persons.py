from uuid import UUID

from pydantic import BaseModel


class PersonFilms(BaseModel):
    uuid: UUID
    roles: list[str]


class PersonModel(BaseModel):
    uuid: UUID
    full_name: str
    films: list[PersonFilms] | None = None
