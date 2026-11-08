import contextlib
from dataclasses import dataclass

from elasticsearch import Elasticsearch

from core.config import settings


@dataclass
class ElasticsearchClient:
    client: Elasticsearch
    
    @classmethod
    def create(cls) -> ElasticsearchClient:
        return cls(
            client=Elasticsearch(
                hosts=[settings.elasticsearch_url, ],
                max_retries=0,
            ),
        )
    
    def reconnect(self) -> None:
        with contextlib.suppress(Exception):
            self.client.close()
        
        self.client = Elasticsearch(
            hosts=[settings.elasticsearch_url, ],
            max_retries=0,
        )
    
    def close(self) -> None:
        self.client.close()
