from uuid import UUID

from pydantic import BaseModel


class PersonFilmModel(BaseModel):
    id: UUID
    roles: list[str]


class Person(BaseModel):
    id: UUID
    full_name: str
    films: list[PersonFilmModel]


class ElasticPersonDocumentModel(BaseModel):
    index: str
    id: UUID
    source: Person
