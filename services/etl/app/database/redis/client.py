from dataclasses import dataclass

from redis import Redis

from core.config import settings


@dataclass
class RedisClient:
    connection: Redis

    @classmethod
    def create(cls) -> RedisClient:
        connection = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            decode_responses=True,
        )

        return cls(connection=connection)

    def close(self) -> None:
        self.connection.close()
