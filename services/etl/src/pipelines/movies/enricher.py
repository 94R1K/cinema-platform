from dataclasses import dataclass
from uuid import UUID

import psycopg
from backoff.decorator import backoff
from core.config import settings
from database.postgres.client import PostgresClient
from models.film_work import (
    FilmWorkEnricherModel,
    GenreFilmWorkEnricherModel,
    PersonFilmWorkEnricherModel,
)
from psycopg.sql import SQL, Literal


@dataclass
class PostgresEnricher:
    postgres: PostgresClient

    @backoff(
        start_sleep_time=settings.backoff_seconds,
        exceptions=(psycopg.OperationalError,),
        reconnect=lambda enricher: enricher.postgres.reconnect(),
    )
    def get_film_works(
        self,
        film_work_ids: set[UUID],
    ) -> list[FilmWorkEnricherModel]:
        if not film_work_ids:
            return []

        query = SQL(
            """
            SELECT
                id,
                title,
                description,
                rating AS imdb_rating
            FROM content.film_work
            WHERE id IN ({film_work_ids});
            """
        ).format(
            film_work_ids=SQL(", ").join(
                Literal(film_work_id) for film_work_id in film_work_ids
            ),
        )

        rows = self.postgres.cursor.execute(query).fetchall()

        return [
            FilmWorkEnricherModel.model_validate(row)
            for row in rows
        ]

    @backoff(
        start_sleep_time=settings.backoff_seconds,
        exceptions=(psycopg.OperationalError,),
        reconnect=lambda enricher: enricher.postgres.reconnect(),
    )
    def get_persons(
        self,
        film_work_ids: set[UUID],
    ) -> list[PersonFilmWorkEnricherModel]:

        if not film_work_ids:
            return []

        query = SQL(
            """
            SELECT
                pfw.film_work_id,
                p.id,
                p.full_name,
                pfw.role
            FROM content.person_film_work pfw
                 JOIN content.person p
                      ON p.id = pfw.person_id
            WHERE pfw.film_work_id IN ({film_work_ids});
            """
        ).format(
            film_work_ids=SQL(", ").join(
                Literal(film_work_id) for film_work_id in film_work_ids
            ),
        )

        rows = self.postgres.cursor.execute(query).fetchall()

        return [
            PersonFilmWorkEnricherModel.model_validate(row)
            for row in rows
        ]

    @backoff(
        start_sleep_time=settings.backoff_seconds,
        exceptions=(psycopg.OperationalError,),
        reconnect=lambda enricher: enricher.postgres.reconnect(),
    )
    def get_genres(
        self,
        film_work_ids: set[UUID],
    ) -> list[GenreFilmWorkEnricherModel]:

        if not film_work_ids:
            return []

        query = SQL(
            """
            SELECT
                gfw.film_work_id,
                g.id,
                g.name
            FROM content.genre_film_work gfw
                 JOIN content.genre g
                      ON g.id = gfw.genre_id
            WHERE gfw.film_work_id IN ({film_work_ids});
            """
        ).format(
            film_work_ids=SQL(", ").join(
                Literal(film_work_id) for film_work_id in film_work_ids
            ),
        )

        rows = self.postgres.cursor.execute(query).fetchall()

        return [
            GenreFilmWorkEnricherModel.model_validate(row)
            for row in rows
        ]
