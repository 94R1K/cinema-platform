from enum import StrEnum


class StateKey(StrEnum):
    MOVIES_FILM_WORK = "movies:film_work"
    MOVIES_PERSON = "movies:person"
    MOVIES_GENRE = "movies:genre"

    PERSONS_PERSON = "persons:person"
    PERSONS_FILM_WORK = "persons:film_work"

    GENRES_GENRE = "genres:genre"
    GENRES_FILM_WORK = "genres:film_work"
