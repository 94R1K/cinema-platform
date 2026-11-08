from pydantic import BaseModel


class ElasticSearchFilmSearchFilter(BaseModel):
    query: str
    page_size: int = 50
    page_number: int = 1
