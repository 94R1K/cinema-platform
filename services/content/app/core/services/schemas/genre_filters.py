from enum import StrEnum

from core.database.schemas import ElasticSearchGenreFilter
from pydantic import BaseModel


class ServiceGenreSortField(StrEnum):
    NAME = "name"


class ServiceGenreFilters(BaseModel):
    sort_by: ServiceGenreSortField | None = None
    sort_direction: str | None = None
    name: str | None = None
    page_size: int = 50
    page_number: int = 1

    def to_elasticsearch_filters(
        self,
    ) -> ElasticSearchGenreFilter:
        sort_field_mapping = {
            ServiceGenreSortField.NAME: "name.raw",
        }

        sort_by = None

        if self.sort_by:
            sort_by = sort_field_mapping[self.sort_by]

        return ElasticSearchGenreFilter(
            sort_by=sort_by,
            sort_direction=self.sort_direction,
            name=self.name,
            page_size=self.page_size,
            page_number=self.page_number,
        )