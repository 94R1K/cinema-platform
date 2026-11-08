from dataclasses import dataclass

from infrastructure.elasticsearch.loader import ElasticsearchLoader
from state.keys import StateKey
from state.state import ETLState

from .enricher import PostgresEnricher
from .merger import FilmWorkMerger
from .producer import PostgresProducer
from .transformer import FilmWorkTransformer


@dataclass
class MoviesPipeline:
    producer: PostgresProducer
    enricher: PostgresEnricher
    merger: FilmWorkMerger
    transformer: FilmWorkTransformer
    loader: ElasticsearchLoader
    state: ETLState
    
    def run_once(self) -> None:
        changed = self.producer.extract(
            film_work_checkpoint=self.state.get_checkpoint(
                StateKey.MOVIES_FILM_WORK
            ),
            person_checkpoint=self.state.get_checkpoint(
                StateKey.MOVIES_PERSON
            ),
            genre_checkpoint=self.state.get_checkpoint(StateKey.MOVIES_GENRE),
        )
        
        film_works = self.enricher.get_film_works(changed.film_work_ids)
        
        persons = self.enricher.get_persons(changed.film_work_ids)
        
        genres = self.enricher.get_genres(changed.film_work_ids)
        
        merged = self.merger.merge(
            film_works=film_works,
            persons=persons,
            genres=genres,
        )
        
        documents = self.transformer.transform_batch(merged)
        
        self.loader.load(documents)
        
        self.state.set_checkpoint(
            StateKey.MOVIES_FILM_WORK,
            changed.film_work_checkpoint,
        )
        
        self.state.set_checkpoint(
            StateKey.MOVIES_PERSON,
            changed.person_checkpoint,
        )
        
        self.state.set_checkpoint(
            StateKey.MOVIES_GENRE,
            changed.genre_checkpoint,
        )
