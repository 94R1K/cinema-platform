from uuid import UUID

from pydantic import BaseModel

from .genres import GenreModel
from .persons import PersonModel


class FilmModel(BaseModel):
    """Модель общей информации о фильме."""

    uuid: UUID
    title: str
    imdb_rating: float | None = None


class FilmDetailModel(FilmModel):
    """Модель детальной информации о фильме."""

    description: str | None = None

    genre: list[GenreModel]
    actors: list[PersonModel]
    writers: list[PersonModel]
    directors: list[PersonModel]
