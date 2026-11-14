import pytest

from tests.core.settings import settings


@pytest.mark.asyncio(loop_scope="session")
async def test_film_search_by_title(client_session):
    """Тест поиска фильма по названию"""

    url = settings.service_url + "/api/v1/films/search"
    params = {
        "query": "Эхо далеких планет"
    }
    async with client_session.get(url, params=params) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert len(body) == 1
    assert body[0]["title"] == "Эхо далеких планет"
    assert body[0]["imdb_rating"] == 7.4


@pytest.mark.asyncio(loop_scope="session")
async def test_film_search_by_wrong_title(client_session):
    """Тест поиска фильма по несуществующему названию"""

    url = settings.service_url + "/api/v1/films/search"
    params = {
        "query": "СуперФИЛЬМ"
    }
    async with client_session.get(url, params=params) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert len(body) == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_film_search_by_persons(client_session):
    """Тест поиска фильма по персоне"""

    url = settings.service_url + "/api/v1/films/search"
    params = {
        "query": "Кристофер Нолан"
    }
    async with client_session.get(url, params=params) as response:
        body = await response.json()
        status = response.status

    film_names = ["Код бесконечности"]

    get_film_names = [film["title"] for film in body]

    assert status == 200
    assert len(body) == 1
    assert film_names == get_film_names


@pytest.mark.asyncio(loop_scope="session")
async def test_film_search_by_wrong_persons(client_session):
    """Тест поиска фильма по несуществующей персоне"""

    url = settings.service_url + "/api/v1/films/search"
    params = {
        "query": "НесуществующийАвторСценаристАктерРежиссер"
    }
    async with client_session.get(url, params=params) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert len(body) == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_film_search_by_description(client_session):
    """Тест поиска фильмов по описанию"""

    url = settings.service_url + "/api/v1/films/search"
    params = {
        "query": "Ученый отправляется за горизонт событий"
    }
    async with client_session.get(url, params=params) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert len(body) == 2
    assert "По ту сторону сингулярности" in [film["title"] for film in body]


@pytest.mark.asyncio(loop_scope="session")
async def test_film_search_by_wrong_description(client_session):
    """Тест поиска фильмов по описанию фильма, которого нет в бд"""

    url = settings.service_url + "/api/v1/films/search"
    params = {
        "query": "ТакогоФильмаЕщеНиктоНеВидел"
    }
    async with client_session.get(url, params=params) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert len(body) == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_person_search_by_part_of_full_name(client_session):
    """Тест поиска персоны по части имени"""

    url = settings.service_url + "/api/v1/persons/search"
    params = {
        "query": "Нолан"
    }
    async with client_session.get(url, params=params) as response:
        body = await response.json()
        status = response.status

    full_names = ["Кристофер Нолан", "Джонатан Нолан"]
    get_full_names = [person["full_name"] for person in body]

    assert status == 200
    assert len(body) == 2
    assert get_full_names == full_names


@pytest.mark.asyncio(loop_scope="session")
async def test_person_search_by_full_name(client_session):
    """Тест поиска персоны по полному имени"""

    url = settings.service_url + "/api/v1/persons/search"
    params = {
        "query": "Квентин Тарантино"
    }
    async with client_session.get(url, params=params) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert len(body) == 1
    assert body[0]["full_name"] == "Квентин Тарантино"


@pytest.mark.asyncio(loop_scope="session")
async def test_person_search_by_wrong_full_name(client_session):
    """Тест поиска персоны по несуществующему имени"""

    url = settings.service_url + "/api/v1/persons/search"
    params = {
        "query": "ТакогоИмениСовсемНет"
    }
    async with client_session.get(url, params=params) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert len(body) == 0
