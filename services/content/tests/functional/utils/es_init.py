import asyncio
import contextlib
import json
import logging
from pathlib import Path

from elasticsearch import AsyncElasticsearch, NotFoundError

logger = logging.getLogger(__name__)


async def prepare_data(es: AsyncElasticsearch, es_index_name: str) -> None:
    logger.info(f"Open {es_index_name}")

    with contextlib.suppress(NotFoundError):
        await es.delete_by_query(
            index=es_index_name,
            query={"match_all": {}},
            refresh=True,
        )

    operations = []

    fixture_path = Path("./fixtures") / f"{es_index_name}.json"
    content = await asyncio.to_thread(
        fixture_path.read_text,
        encoding="utf-8",
    )
    data = json.loads(content)

    for item in data:
        operations.extend(
            [
                {
                    "index": {
                        "_index": es_index_name,
                        "_id": item["id"],
                    }
                },
                item,
            ]
        )

    await es.bulk(
        operations=operations,
        refresh=True,
    )
