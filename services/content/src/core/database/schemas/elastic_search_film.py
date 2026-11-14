from uuid import UUID

from pydantic import BaseModel

from .elastic_search_genre import ElasticSearchGenreModel


class ELasticSearchFilmModel(BaseModel):
    id: UUID
    title: str
    imdb_rating: float | None


class ELasticSearchPersonForFilmsModel(BaseModel):
    id: UUID
    name: str


class ELasticSearchFilmFullModel(ELasticSearchFilmModel):
    description: str | None = None

    genres: list[ElasticSearchGenreModel]
    actors: list[ELasticSearchPersonForFilmsModel]
    writers: list[ELasticSearchPersonForFilmsModel]
    directors: list[ELasticSearchPersonForFilmsModel]
