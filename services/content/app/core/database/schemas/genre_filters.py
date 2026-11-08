from .base_filter import ElasticSearchFilter


class ElasticSearchGenreFilter(ElasticSearchFilter):
    name: str | None = None
