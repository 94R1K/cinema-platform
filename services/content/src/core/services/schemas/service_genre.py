from uuid import UUID

from pydantic import BaseModel


class ServiceGenreModel(BaseModel):
    """Модель жанра."""

    uuid: UUID
    name: str
