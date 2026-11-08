import json
import pytest

from tests.core.settings import settings


@pytest.mark.asyncio(loop_scope="session")
async def test_genres(client_session):
    """Тест получения списка жанров."""
    
    url = settings.service_url + '/api/v1/genres'
    async with client_session.get(url) as response:
        body = await response.json()
        status = response.status

    assert status == 200
    assert len(body) == 50
    for genre in body:
        assert set(genre.keys()) == {"uuid", "name"}


@pytest.mark.asyncio(loop_scope="session")
async def test_genres_get_redis(client_session, redis_client):
    url = settings.service_url + '/api/v1/genres?page_size=50&page_number=1'
    async with client_session.get(url) as response:
        body = await response.json()
        status = response.status
    
    cache_key = "cache:ff250acfb028bf425cac5ef1939586561ba5132f30581df2d30100b851f12f23"
    value = await redis_client.get(cache_key)
    data = json.loads(value)

    assert len(data) == 50
