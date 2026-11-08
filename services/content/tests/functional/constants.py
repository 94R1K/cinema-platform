from typing import Any, Final
from uuid import UUID

from tests.core.settings import settings

PERSON_ID: Final[UUID] = UUID("4044446b-019a-4aa7-87c8-026ae32d76ef")
FILM_ID: Final[UUID] = UUID("dce08875-e6ec-44af-ba8d-8a95d9e6202b")
FILM_2_ID: Final[UUID] = UUID("0d971a9b-f4e8-492e-aad6-3f731961ff3c")
URL_FILMS: str = f"{settings.service_url}/api/v1/films"
EXPECTED_FILM: dict[str, Any] = {
    "uuid": "dce08875-e6ec-44af-ba8d-8a95d9e6202b",
    "title": "По ту сторону сингулярности",
    "imdb_rating": 8.7,
    "description": "Ученый отправляется за горизонт событий, чтобы найти дочь, но возвращается в мир, где время течет в обратную сторону.",
    "genre": [
        {"uuid": "4c1f9a62-8e35-47bd-9210-6a3d5f8072ce", "name": "Фантастика"},
        {"uuid": "6e3b8d02-4f75-49a1-8c26-0d7e5b9381af", "name": "Космическая опера"},
        {"uuid": "0f6b8f2a-91d4-4b77-8e23-5c6a9d1f4072", "name": "Драма"},
    ],
    "actors": [
        {
            "uuid": "4044446b-019a-4aa7-87c8-026ae32d76ef",
            "full_name": "Роберт Дауни мл.",
            "films": None,
        }
    ],
    "writers": [],
    "directors": [],
}
