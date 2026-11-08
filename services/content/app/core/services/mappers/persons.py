from ...database.schemas import ElasticSearchPersonModel
from ..schemas import ServicePersonFilms, ServicePersonModelWithFilms


def service_person_model_from_elastic_search(
    db_person: ElasticSearchPersonModel,
) -> "ServicePersonModelWithFilms":

    return ServicePersonModelWithFilms(
        uuid=db_person.id,
        full_name=db_person.full_name,
        films=[
            ServicePersonFilms(
                uuid=film.id,
                roles=film.roles,
            )
            for film in db_person.films
        ],
    )
