from enum import StrEnum

from pydantic import BaseModel

from core.database.schemas import ElasticSearchPersonFilter


class ServicePersonSortField(StrEnum):
    FULL_NAME = "full_name"


class ServicePersonFilters(BaseModel):
    sort_by: ServicePersonSortField | None = None
    sort_direction: str | None = None
    full_name: str | None = None
    page_size: int = 50
    page_number: int = 1

    def to_elasticsearch_filters(
        self,
    ) -> ElasticSearchPersonFilter:
        sort_field_mapping = {
            ServicePersonSortField.FULL_NAME: "full_name.raw",
        }

        sort_by = None

        if self.sort_by:
            sort_by = sort_field_mapping[self.sort_by]

        return ElasticSearchPersonFilter(
            sort_by=sort_by,
            sort_direction=self.sort_direction,
            full_name=self.full_name,
            page_size=self.page_size,
            page_number=self.page_number,
        )
