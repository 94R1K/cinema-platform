from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

import psycopg
from backoff.decorator import backoff
from core.config import settings
from database.postgres.client import PostgresClient
from psycopg.sql import SQL, Literal
from state.state import Checkpoint


@dataclass
class ChangedGenres:
    genre_ids: set[UUID]
    genre_checkpoint: Checkpoint | None
    film_work_checkpoint: Checkpoint | None


@dataclass
class PostgresProducer:
    postgres: PostgresClient

    @backoff(
        start_sleep_time=settings.backoff_seconds,
        exceptions=(psycopg.OperationalError,),
        reconnect=lambda producer: producer.postgres.reconnect(),
    )
    def extract(
        self,
        genre_checkpoint: Checkpoint | None,
        film_work_checkpoint: Checkpoint | None,
    ) -> ChangedGenres:

        genre_ids, new_genre_checkpoint = self._get_changed_genres(
            genre_checkpoint,
        )

        film_work_ids, new_film_work_checkpoint = self._get_changed_film_works(
            film_work_checkpoint,
        )

        changed_genre_ids = set(genre_ids)
        changed_genre_ids.update(self._get_genres_by_film_works(film_work_ids))

        return ChangedGenres(
            genre_ids=changed_genre_ids,
            genre_checkpoint=new_genre_checkpoint,
            film_work_checkpoint=new_film_work_checkpoint,
        )

    def _get_changed_film_works(
        self,
        checkpoint: Checkpoint | None,
    ) -> tuple[list[UUID], Checkpoint | None]:

        if checkpoint is None:
            modified = datetime.min.replace(tzinfo=UTC)
            last_id = None
        else:
            modified = checkpoint.modified
            last_id = checkpoint.id

        if last_id is None:
            query = SQL(
                """
                SELECT
                    id,
                    modified
                FROM content.film_work
                WHERE modified > {modified}
                ORDER BY modified, id
                LIMIT {batch_size};
                """
            ).format(
                modified=Literal(modified),
                batch_size=Literal(settings.batch_size),
            )
        else:
            query = SQL(
                """
                SELECT
                    id,
                    modified
                FROM content.film_work
                WHERE (modified, id) > (
                    {modified}, {last_id}
                    )
                ORDER BY modified, id
                LIMIT {batch_size};
                """
            ).format(
                modified=Literal(modified),
                last_id=Literal(last_id),
                batch_size=Literal(settings.batch_size),
            )

        rows = self.postgres.cursor.execute(query).fetchall()

        if not rows:
            return [], checkpoint

        last_row = rows[-1]

        return (
            [row["id"] for row in rows],
            Checkpoint(
                modified=last_row["modified"],
                id=last_row["id"],
            ),
        )

    def _get_changed_genres(
        self,
        checkpoint: Checkpoint | None,
    ) -> tuple[list[UUID], Checkpoint | None]:

        if checkpoint is None:
            modified = datetime.min.replace(tzinfo=UTC)
            last_id = None
        else:
            modified = checkpoint.modified
            last_id = checkpoint.id

        if last_id is None:
            query = SQL(
                """
                SELECT
                    id,
                    modified
                FROM content.genre
                WHERE modified > {modified}
                ORDER BY modified, id
                LIMIT {batch_size};
                """
            ).format(
                modified=Literal(modified),
                batch_size=Literal(settings.batch_size),
            )
        else:
            query = SQL(
                """
                SELECT
                    id,
                    modified
                FROM content.genre
                WHERE (modified, id) > (
                    {modified}, {last_id}
                    )
                ORDER BY modified, id
                LIMIT {batch_size};
                """
            ).format(
                modified=Literal(modified),
                last_id=Literal(last_id),
                batch_size=Literal(settings.batch_size),
            )

        rows = self.postgres.cursor.execute(query).fetchall()

        if not rows:
            return [], checkpoint

        last_row = rows[-1]

        return (
            [row["id"] for row in rows],
            Checkpoint(
                modified=last_row["modified"],
                id=last_row["id"],
            ),
        )

    def _get_genres_by_film_works(
        self,
        film_works_ids: list[UUID],
    ) -> list[UUID]:

        if not film_works_ids:
            return []

        query = SQL(
            """
            SELECT DISTINCT
                genre_id
            FROM content.genre_film_work
            WHERE film_work_id IN ({film_work_ids});
            """
        ).format(
            film_work_ids=SQL(", ").join(
                Literal(film_work_id) for film_work_id in film_works_ids
            ),
        )

        rows = self.postgres.cursor.execute(query).fetchall()

        return [row["genre_id"] for row in rows]
