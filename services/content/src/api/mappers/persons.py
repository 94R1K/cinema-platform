from core.services.schemas import ServicePersonModel

from api.schemas import PersonFilms, PersonModel


def service_person_to_api(
    person: ServicePersonModel,
) -> PersonModel:
    return PersonModel(
        uuid=person.uuid,
        full_name=person.full_name,
        films=[
            PersonFilms(
                uuid=film.uuid,
                roles=film.roles
            ) for film in person.films
        ],
    )
