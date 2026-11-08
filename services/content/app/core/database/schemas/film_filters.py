from uuid import UUID

from .base_filter import ElasticSearchFilter


class ElasticSearchFilmFilter(ElasticSearchFilter):
    genre_id: UUID | None = None
