from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import settings
from core.database.postgres import PostgresDatabaseABC

engine = create_async_engine(settings.postgres_url)

async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


class PostgresDatabase(PostgresDatabaseABC):
    async def get_films(self) -> list[Any]:
        ...

    async def get_persons(self) -> list[Any]:
        ...

    async def get_genres(self) -> list[Any]:
        ...
