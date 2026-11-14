from core.services.schemas import ServiceFilmFullModel

from api.schemas import FilmDetailModel, GenreModel, PersonModel


def service_film_to_api(
    film: ServiceFilmFullModel,
) -> FilmDetailModel:
    return FilmDetailModel(
        uuid=film.uuid,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=[
            GenreModel(
                uuid=genre.uuid,
                name=genre.name,
            )
            for genre in film.genres
        ],
        actors=[
            PersonModel(
                uuid=actor.uuid,
                full_name=actor.full_name,
            )
            for actor in film.actors
        ],
        writers=[
            PersonModel(
                uuid=writer.uuid,
                full_name=writer.full_name,
            )
            for writer in film.writers
        ],
        directors=[
            PersonModel(
                uuid=director.uuid,
                full_name=director.full_name,
            )
            for director in film.directors
        ],
    )
