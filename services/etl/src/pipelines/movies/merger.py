from collections import defaultdict
from uuid import UUID

from models.film_work import (
    FilmWorkEnricherModel,
    GenreFilmWorkEnricherModel,
    GenreModel,
    MergedFilmWorkModel,
    PersonFilmWorkEnricherModel,
    PersonModel,
)


class FilmWorkMerger:

    @staticmethod
    def merge(
        film_works: list[FilmWorkEnricherModel],
        persons: list[PersonFilmWorkEnricherModel],
        genres: list[GenreFilmWorkEnricherModel],
    ) -> list[MergedFilmWorkModel]:

        persons_by_film_work: dict[
            UUID, list[PersonModel]
        ] = defaultdict(list)
        genres_by_film_work: dict[
            UUID, list[GenreModel]
        ] = defaultdict(list)

        for person in persons:
            persons_by_film_work[person.film_work_id].append(
                PersonModel(
                    id=person.id,
                    full_name=person.full_name,
                    role=person.role,
                )
            )

        for genre in genres:
            genres_by_film_work[genre.film_work_id].append(
                GenreModel(
                    id=genre.id,
                    name=genre.name
                )
            )

        result: list[MergedFilmWorkModel] = []

        for film_work in film_works:
            film_work_id = film_work.id

            result.append(
                MergedFilmWorkModel(
                    id=film_work_id,
                    title=film_work.title,
                    description=film_work.description,
                    imdb_rating=film_work.imdb_rating,
                    persons=persons_by_film_work.get(
                        film_work_id,
                        [],
                    ),
                    genres=genres_by_film_work.get(
                        film_work_id,
                        [],
                    ),
                )
            )

        return result
