from typing import TYPE_CHECKING, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from api.dependencies import get_person_service

from ..mappers.persons import service_person_to_api
from ..schemas import FilmModel, PersonModel, PersonQueryParams


if TYPE_CHECKING:
    from core.services.persons import PersonServiceABC


person_router = APIRouter(
    prefix="/api/v1",
    tags=["persons"],
    responses={
        404: {"description": "Персона не найдена"},
    },
)


@person_router.get(
    "/persons/search",
    response_model=list[PersonModel],
    summary="Получить список персон",
    description="Возвращает список персон (список фильмов, полное имя и uuid)",
)
async def get_persons(
    query_params: Annotated[PersonQueryParams, Query()],
    service: Annotated[PersonServiceABC, Depends(get_person_service)],
):
    persons = await service.get_persons(query_params.person_query_params_to_filter())

    return [service_person_to_api(person) for person in persons]


@person_router.get(
    "/person/{person_uuid}/",
    response_model=PersonModel,
    summary="Получить персону по uuid",
    description="Возвращает данные по персоне (список фильмов, полное имя и uuid)",
)
async def get_person(
    person_uuid: UUID,
    service: Annotated[PersonServiceABC, Depends(get_person_service)],
):
    if person := await service.get_person_by_uuid(person_uuid):
        return service_person_to_api(person)

    raise HTTPException(
        status_code=404,
        detail="Person not found",
    )


@person_router.get(
    "/persons/{person_uuid}/films",
    response_model=list[FilmModel],
    summary="Получить список фильмов персоны по uuid",
    description="Возвращает список фильмов персоны "
    "(название, идентификатор и рейтинг фильма)",
)
async def person_films_by_uuid(
    person_uuid: UUID,
    service: Annotated[PersonServiceABC, Depends(get_person_service)],
):
    person_films = await service.get_person_films_by_uuid(person_uuid)

    if person_films is not None:
        return [
            FilmModel(
                uuid=film.uuid,
                title=film.title,
                imdb_rating=film.imdb_rating,
            )
            for film in person_films
        ]

    raise HTTPException(
        status_code=404,
        detail="Person not found",
    )
