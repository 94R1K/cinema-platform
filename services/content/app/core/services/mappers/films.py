from ...database.schemas import ELasticSearchFilmFullModel
from ..schemas import (ServiceFilmFullModel, ServiceGenreModel,
                       ServicePersonModel)


def service_film_full_model_from_elastic_search(
    db_film_full_model: ELasticSearchFilmFullModel,
) -> "ServiceFilmFullModel":

    return ServiceFilmFullModel(
        uuid=db_film_full_model.id,
        title=db_film_full_model.title,
        imdb_rating=db_film_full_model.imdb_rating,
        description=db_film_full_model.description,
        genres=[
            ServiceGenreModel(
                uuid=genre.id,
                name=genre.name,
            )
            for genre in db_film_full_model.genres
        ],
        actors=[
            ServicePersonModel(
                uuid=actor.id,
                full_name=actor.name,
            )
            for actor in db_film_full_model.actors
        ],
        writers=[
            ServicePersonModel(
                uuid=writer.id,
                full_name=writer.name,
            )
            for writer in db_film_full_model.writers
        ],
        directors=[
            ServicePersonModel(
                uuid=director.id,
                full_name=director.name,
            )
            for director in db_film_full_model.directors
        ],
    )
