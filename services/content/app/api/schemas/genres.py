from uuid import UUID

from pydantic import BaseModel


class GenreModel(BaseModel):
    uuid: UUID
    name: str
