from core.services.schemas import ServicePersonFilters, ServicePersonSortField
from pydantic import field_validator

from .query_params import PaginationParams


class PersonQueryParams(PaginationParams):
    sort: str | None = None
    query: str | None = None

    @field_validator("sort")
    @classmethod
    def validate_sort(cls, value: str | None) -> str | None:
        if value is None:
            return None

        sort_field = value.removeprefix("-")

        if sort_field not in {
            ServicePersonSortField.FULL_NAME,
        }:
            raise ValueError(f"Invalid sort field: {sort_field}")

        return value

    def person_query_params_to_filter(self) -> ServicePersonFilters:
        sort_by = None
        sort_direction = None

        if self.sort:
            sort_field = self.sort.removeprefix("-")

            sort_by = ServicePersonSortField(sort_field)

            if self.sort.startswith("-"):
                sort_direction = "desc"
            else:
                sort_direction = "asc"

        return ServicePersonFilters(
            sort_by=sort_by,
            sort_direction=sort_direction,
            full_name=self.query,
            page_size=self.page_size,
            page_number=self.page_number,
        )
