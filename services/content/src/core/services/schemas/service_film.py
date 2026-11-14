from uuid import UUID

from pydantic import BaseModel

from .service_genre import ServiceGenreModel
from .service_person import ServicePersonModel


class ServiceFilmModel(BaseModel):
    uuid: UUID
    title: str
    imdb_rating: float | None


class ServiceFilmFullModel(ServiceFilmModel):
    description: str | None = None

    genres: list[ServiceGenreModel]
    actors: list[ServicePersonModel]
    writers: list[ServicePersonModel]
    directors: list[ServicePersonModel]
