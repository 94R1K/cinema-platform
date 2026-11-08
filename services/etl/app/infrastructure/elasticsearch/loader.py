import logging
from dataclasses import dataclass

from elastic_transport import ConnectionError as ElasticConnectionError
from elastic_transport import ConnectionTimeout as ElasticConnectionTimeout
from elasticsearch.helpers import BulkIndexError, bulk

from backoff.decorator import backoff
from core.config import settings
from database.elasticsearch.client import ElasticsearchClient

logger = logging.getLogger(__name__)


@dataclass
class ElasticsearchLoader:
    elasticsearch: ElasticsearchClient

    @backoff(
        start_sleep_time=settings.backoff_seconds,
        exceptions=(
            ElasticConnectionError,
            ElasticConnectionTimeout,
        ),
        reconnect=lambda loader: loader.elasticsearch.reconnect(),
    )
    def load[T](self, documents: list[T]) -> None:
        if not documents:
            return

        actions = [
            {
                "_index": document.index,
                "_id": str(document.id),
                **document.source.model_dump(mode="json"),
            }
            for document in documents
        ]

        try:
            bulk(
                self.elasticsearch.client,
                actions,
            )
        except BulkIndexError as exc:
            logger.error(
                "Не удалось загрузить %d документов",
                len(exc.errors),
            )

            for error in exc.errors[:3]:
                logger.error("Ошибка Elasticsearch: %s", error)

            raise
