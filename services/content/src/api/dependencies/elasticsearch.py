from typing import Annotated

from db import ElasticSearchDatabase
from elasticsearch import AsyncElasticsearch
from fastapi import Depends, Request


def get_elasticsearch(request: Request) -> AsyncElasticsearch:
    return request.app.state.elasticsearch


def get_elastic_search_database(
    elastic_search_client: Annotated[
        AsyncElasticsearch,
        Depends(get_elasticsearch),
    ],
) -> ElasticSearchDatabase:
    return ElasticSearchDatabase(
        elastic_search_client=elastic_search_client,
    )
