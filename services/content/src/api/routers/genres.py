from typing import TYPE_CHECKING, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from ..dependencies import get_genre_service
from ..schemas import GenreModel, GenreQueryParams


if TYPE_CHECKING:
    from core.services.genre import GenreServiceABC


genre_router = APIRouter(
    prefix="/api/v1",
    tags=["genres"],
    responses={
        404: {"description": "Жанр не найден"},
    },
)


@genre_router.get(
    "/genres",
    response_model=list[GenreModel],
    summary="Получить список жанров",
    description="Возвращет список жанров (название и uuid)",
)
async def get_genres(
    query_params: Annotated[GenreQueryParams, Query()],
    service: Annotated[GenreServiceABC, Depends(get_genre_service)],
):
    genres = await service.get_genres(query_params.genre_query_params_to_filter())

    return [
        GenreModel(
            uuid=genre.uuid,
            name=genre.name,
        )
        for genre in genres
    ]


@genre_router.get(
    "/genres/{genre_uuid}",
    response_model=GenreModel,
    summary="Получить жанр по uuid",
    description="Возвращет жанр (название и uuid)",
)
async def genre_by_uuid(
    genre_uuid: UUID,
    service: Annotated[GenreServiceABC, Depends(get_genre_service)],
):
    if genre := await service.get_genre_by_uuid(genre_uuid):

        return GenreModel(
            uuid=genre.uuid,
            name=genre.name,
        )

    raise HTTPException(
            status_code=404,
            detail="Genre not found",
        )
