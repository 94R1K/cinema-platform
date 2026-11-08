from pydantic import BaseModel


class ElasticSearchFilter(BaseModel):
    sort_by: str | None = None
    sort_direction: str | None = None
    page_size: int = 50
    page_number: int = 1
