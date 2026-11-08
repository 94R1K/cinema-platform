from models.film_work import (
    ElasticMovieDocumentModel,
    ElasticMoviesPersonModel,
    MergedFilmWorkModel,
    MovieDocumentModel,
)
from pipelines.common.base_transformer import BaseElasticTransformer


class FilmWorkTransformer(
    BaseElasticTransformer[MergedFilmWorkModel, ElasticMovieDocumentModel,],
):
    
    def transform(
        self, film_work: MergedFilmWorkModel,
    ) -> ElasticMovieDocumentModel:
        persons = film_work.persons
        
        directors = [
            ElasticMoviesPersonModel(
                id=person.id,
                name=person.full_name,
            )
            for person in persons
            if person.role == "director"
        ]
        
        actors = [
            ElasticMoviesPersonModel(
                id=person.id,
                name=person.full_name,
            )
            for person in persons
            if person.role == "actor"
        ]
        
        writers = [
            ElasticMoviesPersonModel(
                id=person.id,
                name=person.full_name,
            )
            for person in persons
            if person.role == "writer"
        ]
        
        return ElasticMovieDocumentModel(
            index="movies",
            id=film_work.id,
            source=MovieDocumentModel(
                id=film_work.id,
                title=film_work.title,
                description=film_work.description,
                imdb_rating=film_work.imdb_rating,
                genres=film_work.genres,
                directors_names=[
                    person.full_name
                    for person in persons
                    if person.role == "director"
                ],
                actors_names=[
                    person.full_name
                    for person in persons
                    if person.role == "actor"
                ],
                writers_names=[
                    person.full_name
                    for person in persons
                    if person.role == "writer"
                ],
                directors=directors,
                actors=actors,
                writers=writers,
            ),
        )
