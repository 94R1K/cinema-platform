from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class NamedEntityModel(BaseModel):
    id: UUID
    name: str


class FullNameEntityModel(BaseModel):
    id: UUID
    full_name: str


class FilmWorkEnricherModel(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    imdb_rating: float | int | None = None


class PersonModel(FullNameEntityModel):
    role: Literal['actor', 'director', 'writer']


class PersonFilmWorkEnricherModel(PersonModel):
    film_work_id: UUID


class GenreModel(NamedEntityModel):
    pass


class GenreFilmWorkEnricherModel(GenreModel):
    film_work_id: UUID


class MergedFilmWorkModel(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    imdb_rating: float | int | None = None
    persons: list[PersonModel]
    genres: list[GenreModel]


class ElasticMoviesPersonModel(NamedEntityModel):
    pass


class MovieDocumentModel(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    imdb_rating: float | int | None = None
    genres: list[GenreModel]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    directors: list[ElasticMoviesPersonModel]
    actors: list[ElasticMoviesPersonModel]
    writers: list[ElasticMoviesPersonModel]


class ElasticMovieDocumentModel(BaseModel):
    index: str
    id: UUID
    source: MovieDocumentModel
