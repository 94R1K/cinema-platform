import pytest

from tests.core.settings import settings

from ..constants import FILM_2_ID, FILM_ID, PERSON_ID


@pytest.mark.asyncio(loop_scope="session")
async def test_persons_search(client_session):
    """Тест поиска персон."""
    url = f"{settings.service_url}/api/v1/persons/search"
    params = {
        "query": "Роберт Дауни",
    }
    async with client_session.get(url, params=params) as response:
        body = await response.json()
        status = response.status

        assert status == 200
        assert len(body) == 1
        person = body[0]
        assert set(person.keys()) == {"uuid", "full_name", "films"}
        assert person["uuid"] == str(PERSON_ID)
        assert person["full_name"] == "Роберт Дауни мл."
        assert len(person["films"]) == 2
        for film in person["films"]:
            assert set(film.keys()) == {"uuid", "roles"}


@pytest.mark.asyncio(loop_scope="session")
async def test_persons_search_by_partial_name(client_session):
    """Тест поиска персон по части имени."""

    url = f"{settings.service_url}/api/v1/persons/search"

    params = {
        "query": "Дауни",
    }

    async with client_session.get(url, params=params) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert len(body) == 1
    assert body[0]["uuid"] == str(PERSON_ID)


@pytest.mark.asyncio(loop_scope="session")
async def test_persons_search_not_found(client_session):
    """Тест поиска персон, когда ничего не найдено."""

    url = f"{settings.service_url}/api/v1/persons/search"

    params = {
        "query": "Несуществующий человек",
    }

    async with client_session.get(url, params=params) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert body == []


@pytest.mark.asyncio(loop_scope="session")
async def test_person(client_session):
    """Тест получения информации о персоне."""

    url = f"{settings.service_url}/api/v1/person/{PERSON_ID}/"

    async with client_session.get(url) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert set(body.keys()) == {"uuid", "full_name", "films"}

    assert body["uuid"] == str(PERSON_ID)
    assert body["full_name"] == "Роберт Дауни мл."

    assert len(body["films"]) == 2

    for film in body["films"]:
        assert set(film.keys()) == {"uuid", "roles"}
        assert isinstance(film["uuid"], str)
        assert isinstance(film["roles"], list)
        assert all(isinstance(role, str) for role in film["roles"])


@pytest.mark.asyncio(loop_scope="session")
async def test_person_films(client_session):
    """Тест получения фильмов по персоне."""

    url = f"{settings.service_url}/api/v1/persons/{PERSON_ID}/films"

    async with client_session.get(url) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert len(body) == 2

    for film in body:
        assert set(film.keys()) == {"uuid", "title", "imdb_rating"}
        assert isinstance(film["uuid"], str)
        assert isinstance(film["title"], str)
        assert isinstance(film["imdb_rating"], float)

    film_ids = {film["uuid"] for film in body}

    assert film_ids == {str(FILM_ID), str(FILM_2_ID)}
