from pydantic import BaseModel

from ...database.schemas import ElasticSearchFilmSearchFilter


class ServiceFilmSearchFilters(BaseModel):
    query: str
    page_size: int = 50
    page_number: int = 1

    def to_elasticsearch_filters(self) -> ElasticSearchFilmSearchFilter:
        return ElasticSearchFilmSearchFilter(
            query=self.query,
            page_size=self.page_size,
            page_number=self.page_number,
        )
