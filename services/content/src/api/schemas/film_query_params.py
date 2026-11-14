from enum import StrEnum
from uuid import UUID

from core.services.schemas import ServiceFilmFilters, ServiceFilmSortField
from pydantic import field_validator

from .query_params import PaginationParams


class FilmSortField(StrEnum):
    IMDB_RATING = "imdb_rating"
    TITLE = "title"


class FilmQueryParams(PaginationParams):
    sort: str | None = None
    genre: UUID | None = None

    @field_validator("sort")
    @classmethod
    def validate_sort(cls, value: str | None) -> str | None:
        if value is None:
            return None

        sort_field = value.removeprefix("-")

        if sort_field not in {
            FilmSortField.IMDB_RATING,
            FilmSortField.TITLE,
        }:
            raise ValueError(f"Invalid sort field: {sort_field}")

        return value

    def film_query_params_to_filter(self) -> ServiceFilmFilters:
        sort_by = None
        sort_direction = None

        if self.sort:
            sort_field = self.sort.removeprefix("-")
            sort_by = ServiceFilmSortField(sort_field)
            sort_direction = "desc" if self.sort.startswith("-") else "asc"

        return ServiceFilmFilters(
            sort_by=sort_by,
            sort_direction=sort_direction,
            genre_id=self.genre,
            page_size=self.page_size,
            page_number=self.page_number,
        )
