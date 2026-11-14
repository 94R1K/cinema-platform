from dataclasses import dataclass
from uuid import UUID

import psycopg
from backoff.decorator import backoff
from core.config import settings
from database.postgres.client import PostgresClient
from models.genre import Genre
from psycopg.sql import SQL, Literal


@dataclass
class PostgresReader:
    postgres: PostgresClient

    @backoff(
        start_sleep_time=settings.backoff_seconds,
        exceptions=(psycopg.OperationalError,),
        reconnect=lambda enricher: enricher.postgres.reconnect(),
    )
    def get_genres(
        self,
        genre_ids: set[UUID],
    ) -> list[Genre]:

        if not genre_ids:
            return []

        query = SQL(
            """
            SELECT DISTINCT
                g.id,
                g.name
            FROM content.genre g
                 JOIN content.genre_film_work gfw
                      ON g.id = gfw.genre_id
            WHERE gfw.genre_id IN ({genre_ids});
            """
        ).format(
            genre_ids=SQL(", ").join(
                Literal(genre_id) for genre_id in genre_ids
            ),
        )

        rows = self.postgres.cursor.execute(query).fetchall()

        return [
            Genre.model_validate(row)
            for row in rows
        ]
