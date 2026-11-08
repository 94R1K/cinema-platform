from models.person import ElasticPersonDocumentModel, Person
from pipelines.common.base_transformer import BaseElasticTransformer


class PersonTransformer(
    BaseElasticTransformer[Person, ElasticPersonDocumentModel,],
):
    
    def transform(self, person: Person) -> ElasticPersonDocumentModel:
        return ElasticPersonDocumentModel(
            index="persons",
            id=person.id,
            source=Person(
                id=person.id,
                full_name=person.full_name,
                films=person.films,
            ),
        )
