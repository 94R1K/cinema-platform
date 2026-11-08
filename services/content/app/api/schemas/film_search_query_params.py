from core.services.schemas import ServiceFilmSearchFilters

from .query_params import PaginationParams


class FilmSearchQueryParams(PaginationParams):
    query: str

    def to_service_filters(self) -> ServiceFilmSearchFilters:
        return ServiceFilmSearchFilters(
            query=self.query,
            page_size=self.page_size,
            page_number=self.page_number,
        )
