from .base_filter import ElasticSearchFilter


class ElasticSearchPersonFilter(ElasticSearchFilter):
    full_name: str | None = None
