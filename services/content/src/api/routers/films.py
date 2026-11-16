from typing import TYPE_CHECKING, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from api.dependencies import get_film_service

from ..mappers.films import service_film_to_api
from ..schemas import FilmDetailModel, FilmModel, FilmQueryParams, FilmSearchQueryParams


if TYPE_CHECKING:
    from core.services.film import FilmServiceABC


film_router = APIRouter(
    prefix="/api/v1",
    tags=["films"],
    responses={404: {"description": "Фильм не найден"}},
)


@film_router.get(
    "/films",
    response_model=list[FilmModel],
    summary="Получить список фильмов",
    description="Возвращает список фильмов (uuid, рейтинг и название)",
)
async def get_films(
    query_params: Annotated[FilmQueryParams, Query()],
    service: Annotated[FilmServiceABC, Depends(get_film_service)],
):
    films = await service.get_films(query_params.film_query_params_to_filter())

    return [
        FilmModel(
            uuid=film.uuid,
            title=film.title,
            imdb_rating=film.imdb_rating,
        )
        for film in films
    ]


@film_router.get(
    "/films/{film_id}/",
    response_model=FilmDetailModel,
    summary="Получить фильм по uuid",
    description="Возвращает фильм (uuid, рейтинг и название)",
)
async def get_film(
    film_id: UUID,
    service: Annotated[FilmServiceABC, Depends(get_film_service)],
):
    film = await service.get_film_by_id(film_id)

    if film is None:
        raise HTTPException(
            status_code=404,
            detail="Film not found",
        )

    return service_film_to_api(film)


@film_router.get(
    "/films/search",
    response_model=list[FilmModel],
    summary="Поиск по фильмам",
    description="Возвращает список фильмов по заданным параметрам",
)
async def search_films(
    query_params: Annotated[FilmSearchQueryParams, Query()],
    service: Annotated[FilmServiceABC, Depends(get_film_service)],
):
    films = await service.search_films(
        query_params.to_service_filters(),
    )

    return [
        FilmModel(
            uuid=film.uuid,
            title=film.title,
            imdb_rating=film.imdb_rating,
        )
        for film in films
    ]
