import json
from typing import Any

import pytest
from aiohttp import ClientSession
from redis.asyncio import Redis

from ..constants import EXPECTED_FILM, FILM_ID, URL_FILMS


async def assert_films_response(
    client_session: ClientSession,
    parameters: dict[str, str],
    expected_answer: dict[str, int | None],
) -> list[dict[str, Any]] | None:
    """Проверить ответ эндпоинта со списком фильмов."""
    async with client_session.get(URL_FILMS, params=parameters) as response:
        films = await response.json()
        status = response.status

    assert status == expected_answer["status"]

    if status == 422:
        assert "detail" in films
        return None

    assert len(films) == expected_answer["length"]
    return films


@pytest.mark.parametrize(
    ("parameter", "expected_answer", ),
    [
        (
            {"sort": "-imdb_rating", },
            {"status": 200, "length": 50, },
        ),
        (
            {"sort": "imdb_rating", },
            {"status": 200, "length": 50, },
        ),
        (
            {"sort": "-title", },
            {"status": 200, "length": 50, },
        ),
        (
            {"sort": "title", },
            {"status": 200, "length": 50, },
        ),
        (
            {"sort": "--title", },
            {"status": 422, "length": None, },
        ),
        (
            {"sort": "TITLE", },
            {"status": 422, "length": None, },
        ),
        (
            {"sort": "title ", },
            {"status": 422, "length": None, },
        ),
        (
            {"sort": "0", },
            {"status": 422, "length": None, },
        ),
        (
            {"sort": "1", },
            {"status": 422, "length": None, },
        ),
        (
            {"sort": "-1", },
            {"status": 422, "length": None, },
        ),
        (
            {"sort": "", },
            {"status": 422, "length": None, },
        ),
        (
            {"sort": "unknown_field", },
            {"status": 422, "length": None, },
        ),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_sort_parameter_films(
    client_session: ClientSession,
    parameter: dict[str, str],
    expected_answer: dict[str, int | None],
) -> None:
    """Тест sort параметра."""
    films = await assert_films_response(
        client_session,
        parameter,
        expected_answer,
    )

    if films is None:
        return

    sort = parameter["sort"]

    if isinstance(sort, str) and sort.lstrip("-") in {
        "imdb_rating",
        "title",
    }:
        field = sort.removeprefix("-")
        reverse = sort.startswith("-")

        values = [film[field] for film in films]
        assert values == sorted(values, reverse=reverse)


@pytest.mark.parametrize(
    ("parameter", "expected_answer", ),
    [
        (
            {"genre": "0f6b8f2a-91d4-4b77-8e23-5c6a9d1f4072", },
            {"status": 200, "length": 50, },
        ),
        (
            {"genre": "7f4c9e13-5a86-42b0-9d31-2e6a8c7054bf", },
            {"status": 200, "length": 1, },
        ),
        (
            {"genre": "00000000-0000-0000-0000-000000000000", },
            {"status": 200, "length": 0, },
        ),
        (
            {"genre": "0f6b8f2a-91d4"},
            {"status": 422, "length": None}
        ),
        (
            {"genre": "1"},
            {"status": 422, "length": None, },
        ),
        (
            {"genre": "0"},
            {"status": 422, "length": None, },
        ),
        (
            {"genre": "-1"},
            {"status": 422, "length": None, },
        ),
        (
            {"genre": "", },
            {"status": 422, "length": None, },
        ),
        (
            {"genre": "not-uuid", },
            {"status": 422, "length": None, },
        ),
    ]
)
@pytest.mark.asyncio(loop_scope="session")
async def test_genre_parameter_films(
    client_session: ClientSession,
    parameter: dict[str, str],
    expected_answer: dict[str, int | None],
) -> None:
    """Тест genre параметра."""

    await assert_films_response(
        client_session,
        parameter,
        expected_answer,
    )


@pytest.mark.parametrize(
    ("parameter", "expected_answer", ),
    [
        (
            {"page_size": "50", },
            {"status": 200, "length": 50, },
        ),
        (
            {"page_size": "1", },
            {"status": 200, "length": 1, },
        ),
        (
            {"page_size": "100", },
            {"status": 200, "length": 100, },
        ),
        (
            {"page_size": "1.5", },
            {"status": 422, "length": None, },
        ),
        (
            {"page_size": "101", },
            {"status": 422, "length": None, },
        ),
        (
            {"page_size": "0", },
            {"status": 422, "length": None, },
        ),
        (
            {"page_size": "-1", },
            {"status": 422, "length": None, },
        ),
        (
            {"page_size": "", },
            {"status": 422, "length": None, },
        ),
        (
            {"page_size": "not_an_integer", },
            {"status": 422, "length": None, },
        ),
    ]
)
@pytest.mark.asyncio(loop_scope="session")
async def test_page_size_parameter_films(
    client_session: ClientSession,
    parameter: dict[str, str],
    expected_answer: dict[str, int | None],
) -> None:
    """Тест page_size параметра."""

    await assert_films_response(
        client_session,
        parameter,
        expected_answer,
    )


@pytest.mark.parametrize(
    ("parameters", "expected_answer", ),
    [
        (
            {"page_number": "1", },
            {"status": 200, "length": 50, },
        ),
        (
            {"page_number": "200", },
            {"status": 200, "length": 0, },
        ),
        (
            {"page_number": "201", },
            {"status": 422, "length": None, },
        ),
        (
            {"page_number": "0", },
            {"status": 422, "length": None, },
        ),
        (
            {"page_number": "-1", },
            {"status": 422, "length": None, },
        ),
        (
            {"page_number": "", },
            {"status": 422, "length": None, },
        ),
        (
            {"page_number": "not_an_integer", },
            {"status": 422, "length": None, },
        ),
    ]
)
@pytest.mark.asyncio(loop_scope="session")
async def test_page_number_parameter_films(
    client_session: ClientSession,
    parameters: dict[str, str],
    expected_answer: dict[str, int | None],
) -> None:
    """Тест page_number параметра."""

    await assert_films_response(
        client_session,
        parameters,
        expected_answer,
    )


@pytest.mark.parametrize(
    ("parameters", "expected_answer"),
    [
        (
            {"page_number": "100", "page_size": "100"},
            {"status": 200, "length": 0},
        ),
        (
            {"page_number": "101", "page_size": "100"},
            {"status": 422, "length": None},
        ),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_pagination_result_window(
    client_session: ClientSession,
    parameters: dict[str, str],
    expected_answer: dict[str, int | None],
) -> None:
    """Тест предельного окна результатов Elasticsearch."""
    await assert_films_response(
        client_session,
        parameters,
        expected_answer,
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_films(client_session: ClientSession, ) -> None:
    """Тест получения всех фильмов."""
    page_size = 100
    page_number = 1
    all_films = []

    while True:
        async with client_session.get(
            URL_FILMS,
            params={
                "page_size": page_size,
                "page_number": page_number,
            },
        ) as response:
            assert response.status == 200
            films = await response.json()

        if not films:
            break

        all_films.extend(films)
        page_number += 1

        if page_number * page_size > 10_000:
            pytest.fail(
                "Не удалось проверить получение всех фильмов: "
                "достигнут лимит окна результатов Elasticsearch"
            )

    assert all_films

    for film in all_films:
        assert film.keys() == {
            "uuid",
            "title",
            "imdb_rating",
        }


@pytest.mark.asyncio(loop_scope="session")
async def test_get_films_default_params(client_session: ClientSession, ) -> None:
    """Тест получения фильмов с параметрами по умолчанию."""
    films = await assert_films_response(
        client_session,
        parameters={},
        expected_answer={"status": 200, "length": 50},
    )

    assert films is not None

    for film in films:
        assert film.keys() == {
            "uuid",
            "title",
            "imdb_rating",
        }


@pytest.mark.parametrize(
    ("film_id", "expected_status", ),
    [
        (
            FILM_ID,
            200,
        ),
        (
            "0f6b8f2a-91d4",
            422,
        ),
        (
            "not-uuid",
            422,
        ),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_film_by_uuid(
    client_session: ClientSession,
    film_id: str,
    expected_status: int,
) -> None:
    """Тест получения конкретного фильма."""
    async with client_session.get(f"{URL_FILMS}/{film_id}/") as response:
        film = await response.json()
        status = response.status
    
    assert status == expected_status
    
    if status == 422:
        assert "detail" in film
        return
    
    assert film == EXPECTED_FILM


@pytest.mark.asyncio(loop_scope="session")
async def test_get_films_default_params_redis(
    client_session: ClientSession,
    redis_client: Redis,
) -> None:
    """Тест получения фильмов с параметрами по умолчанию из кэша Redis."""
    films = await assert_films_response(
        client_session,
        parameters={},
        expected_answer={"status": 200, "length": 50},
    )

    redis_key = "cache:c1dcc7b4620283890ad2241d2c5ea8b11881f64b96576fbdf66b2604c0e3676e"
    redis_value = await redis_client.get(redis_key)
    films_redis = json.loads(redis_value)

    assert len(films_redis) == 50
    normalize_films_redis = [
        {
            ("uuid" if key == "id" else key): value
            for key, value in film.items()
        }
        for film in films_redis
    ]
    assert films == normalize_films_redis
