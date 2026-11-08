from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

import psycopg
from psycopg.sql import SQL, Literal

from backoff.decorator import backoff
from core.config import settings
from database.postgres.client import PostgresClient
from state.state import Checkpoint


@dataclass
class ChangedPersons:
    person_ids: set[UUID]
    person_checkpoint: Checkpoint | None
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
        person_checkpoint: Checkpoint | None,
        film_work_checkpoint: Checkpoint | None,
    ) -> ChangedPersons:
        
        person_ids, new_person_checkpoint = self._get_changed_persons(
            person_checkpoint,
        )
        
        film_work_ids, new_film_work_checkpoint = self._get_changed_film_works(
            film_work_checkpoint,
        )
        
        changed_person_ids = set(person_ids)
        changed_person_ids.update(
            self._get_persons_by_film_works(film_work_ids)
        )
        
        return ChangedPersons(
            person_ids=changed_person_ids,
            person_checkpoint=new_person_checkpoint,
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
    
    def _get_changed_persons(
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
                FROM content.person
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
                FROM content.person
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
    
    def _get_persons_by_film_works(
        self,
        film_work_ids: list[UUID],
    ) -> list[UUID]:
        
        if not film_work_ids:
            return []
        
        query = SQL(
            """
            SELECT DISTINCT
                person_id
            FROM content.person_film_work
            WHERE film_work_id IN ({film_work_ids});
            """
        ).format(
            film_work_ids=SQL(", ").join(
                Literal(film_work_id) for film_work_id in film_work_ids
            ),
        )
        
        rows = self.postgres.cursor.execute(query).fetchall()
        
        return [row["person_id"] for row in rows]
