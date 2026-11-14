from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel

from core.database.schemas import ElasticSearchFilmFilter


class ServiceFilmSortField(StrEnum):
    TITLE = "title"
    IMDB_RATING = "imdb_rating"


class ServiceFilmFilters(BaseModel):
    sort_by: ServiceFilmSortField | None = None
    sort_direction: str | None = None
    genre_id: UUID | None = None
    page_size: int = 50
    page_number: int = 1

    def to_elasticsearch_filters(
        self,
    ) -> ElasticSearchFilmFilter:
        sort_field_mapping = {
            ServiceFilmSortField.TITLE: "title.raw",
            ServiceFilmSortField.IMDB_RATING: "imdb_rating",
        }

        sort_by = None

        if self.sort_by:
            sort_by = sort_field_mapping[self.sort_by]

        return ElasticSearchFilmFilter(
            sort_by=sort_by,
            sort_direction=self.sort_direction,
            genre_id=self.genre_id,
            page_size=self.page_size,
            page_number=self.page_number,
        )
