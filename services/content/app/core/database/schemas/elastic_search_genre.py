from uuid import UUID

from pydantic import BaseModel


class ElasticSearchGenreModel(BaseModel):
    """Модель жанра."""

    id: UUID
    name: str
