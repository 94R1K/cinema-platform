import contextlib
from dataclasses import dataclass

import psycopg
from psycopg.rows import dict_row

from core.config import settings


@dataclass
class PostgresClient:
    connection: psycopg.Connection
    cursor: psycopg.ClientCursor

    @staticmethod
    def _create_connection() -> psycopg.Connection:
        return psycopg.connect(
            dbname=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password.get_secret_value(),
            host=settings.postgres_host,
            port=settings.postgres_port,
            row_factory=dict_row,
            cursor_factory=psycopg.ClientCursor,
        )

    @classmethod
    def create(cls) -> PostgresClient:
        connection = cls._create_connection()

        return cls(
            connection=connection,
            cursor=connection.cursor(),
        )

    def reconnect(self) -> None:
        with contextlib.suppress(psycopg.Error):
            self.connection.close()

        self.connection = self._create_connection()
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        self.connection.close()
