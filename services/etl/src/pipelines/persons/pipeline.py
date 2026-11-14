from dataclasses import dataclass

from infrastructure.elasticsearch.loader import ElasticsearchLoader
from state.keys import StateKey
from state.state import ETLState

from .producer import PostgresProducer
from .reader import PostgresReader
from .transformer import PersonTransformer


@dataclass
class PersonsPipeline:
    producer: PostgresProducer
    reader: PostgresReader
    transformer: PersonTransformer
    loader: ElasticsearchLoader
    state: ETLState

    def run_once(self) -> None:
        changed = self.producer.extract(
            person_checkpoint=self.state.get_checkpoint(
                StateKey.PERSONS_PERSON
            ),
            film_work_checkpoint=self.state.get_checkpoint(
                StateKey.PERSONS_FILM_WORK
            ),
        )

        persons = self.reader.get_persons(changed.person_ids)

        documents = self.transformer.transform_batch(persons)

        self.loader.load(documents)

        self.state.set_checkpoint(
            StateKey.PERSONS_PERSON,
            changed.person_checkpoint,
        )

        self.state.set_checkpoint(
            StateKey.PERSONS_FILM_WORK,
            changed.film_work_checkpoint,
        )
