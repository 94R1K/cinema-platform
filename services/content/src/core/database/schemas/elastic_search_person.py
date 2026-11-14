from uuid import UUID

from pydantic import BaseModel


class ElasticSearchPersonFilmsModel(BaseModel):
    id: UUID
    roles: list[str]

class ElasticSearchPersonModel(BaseModel):
    """Модель персоны."""

    id: UUID
    full_name: str
    films: list[ElasticSearchPersonFilmsModel] | None = None
