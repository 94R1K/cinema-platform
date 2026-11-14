import logging
from contextlib import closing

from database.elasticsearch.client import ElasticsearchClient
from database.postgres.client import PostgresClient
from database.redis.client import RedisClient
from infrastructure.elasticsearch.loader import ElasticsearchLoader
from pipelines.genres.pipeline import GenresPipeline
from pipelines.genres.producer import PostgresProducer as GenrePostgresProducer
from pipelines.genres.reader import PostgresReader as GenrePostgresReader
from pipelines.genres.transformer import GenreTransformer
from pipelines.movies.enricher import (
    PostgresEnricher as FilmWorkPostgresEnricher,
)
from pipelines.movies.merger import FilmWorkMerger
from pipelines.movies.pipeline import MoviesPipeline
from pipelines.movies.producer import (
    PostgresProducer as FilmWorkPostgresProducer,
)
from pipelines.movies.transformer import FilmWorkTransformer
from pipelines.orchestrator import ETLOrchestrator
from pipelines.persons.pipeline import PersonsPipeline
from pipelines.persons.producer import (
    PostgresProducer as PersonPostgresProducer,
)
from pipelines.persons.reader import (
    PostgresReader as PersonPostgresReader,
)
from pipelines.persons.transformer import PersonTransformer
from state.state import ETLState
from state.storage import RedisStorage


logger = logging.getLogger(__name__)


def main() -> None:
    with (
        closing(PostgresClient.create()) as postgres,
        closing(ElasticsearchClient.create()) as elasticsearch,
        closing(RedisClient.create()) as redis,
    ):
        storage = RedisStorage(redis)
        state = ETLState(storage)

        film_work_postgres_producer = FilmWorkPostgresProducer(
            postgres=postgres,
        )
        person_postgres_producer = PersonPostgresProducer(
            postgres=postgres,
        )
        genre_postgres_producer = GenrePostgresProducer(
            postgres=postgres,
        )

        film_work_postgres_enricher = FilmWorkPostgresEnricher(
            postgres=postgres,
        )

        person_postgres_reader = PersonPostgresReader(
            postgres=postgres,
        )
        genre_postgres_reader = GenrePostgresReader(
            postgres=postgres,
        )

        film_work_merger = FilmWorkMerger()

        film_work_transformer = FilmWorkTransformer()
        person_transformer = PersonTransformer()
        genre_transformer = GenreTransformer()

        loader = ElasticsearchLoader(
            elasticsearch=elasticsearch,
        )

        movies_pipeline = MoviesPipeline(
            producer=film_work_postgres_producer,
            enricher=film_work_postgres_enricher,
            merger=film_work_merger,
            transformer=film_work_transformer,
            loader=loader,
            state=state,
        )

        persons_pipeline = PersonsPipeline(
            producer=person_postgres_producer,
            reader=person_postgres_reader,
            transformer=person_transformer,
            loader=loader,
            state=state,
        )

        genre_pipeline = GenresPipeline(
            producer=genre_postgres_producer,
            reader=genre_postgres_reader,
            transformer=genre_transformer,
            loader=loader,
            state=state,
        )

        etl = ETLOrchestrator(
            movies=movies_pipeline,
            persons=persons_pipeline,
            genres=genre_pipeline,
        )

        etl.run()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception(
            "Ошибка при переносе данных из PostgreSQL в Elasticsearch",
        )
        raise
