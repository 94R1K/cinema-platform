from collections import defaultdict
from dataclasses import dataclass
from uuid import UUID

import psycopg
from psycopg.sql import SQL, Literal

from backoff.decorator import backoff
from core.config import settings
from database.postgres.client import PostgresClient
from models.person import Person, PersonFilmModel


@dataclass
class PostgresReader:
    postgres: PostgresClient
    
    @backoff(
        start_sleep_time=settings.backoff_seconds,
        exceptions=(psycopg.OperationalError,),
        reconnect=lambda enricher: enricher.postgres.reconnect(),
    )
    def get_persons(
        self,
        person_ids: set[UUID],
    ) -> list[Person]:
        
        if not person_ids:
            return []
        
        query = SQL(
            """
            SELECT DISTINCT
                p.id,
                p.full_name,
                pfw.film_work_id,
                pfw.role
            FROM content.person p
                 JOIN content.person_film_work pfw
                      ON p.id = pfw.person_id
            WHERE pfw.person_id IN ({person_ids});
            """
        ).format(
            person_ids=SQL(", ").join(
                Literal(person_id) for person_id in person_ids
            ),
        )
        
        rows = self.postgres.cursor.execute(query).fetchall()
        
        persons = defaultdict(
            lambda: {
                "full_name": "",
                "films": defaultdict(list),
            }
        )
        
        for row in rows:
            person = persons[row["id"]]
            
            person["full_name"] = row["full_name"]
            person["films"][row["film_work_id"]].append(row["role"])
        
        return [
            Person(
                id=person_id,
                full_name=data["full_name"],
                films=[
                    PersonFilmModel(
                        id=film_id,
                        roles=roles,
                    )
                    for film_id, roles in data["films"].items()
                ],
            )
            for person_id, data in persons.items()
        ]
