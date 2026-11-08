from dataclasses import dataclass

from infrastructure.elasticsearch.loader import ElasticsearchLoader
from models.genre import ElasticGenreDocumentModel, Genre
from state.keys import StateKey
from state.state import ETLState

from .producer import ChangedGenres, PostgresProducer
from .reader import PostgresReader
from .transformer import GenreTransformer


@dataclass
class GenresPipeline:
    producer: PostgresProducer
    reader: PostgresReader
    transformer: GenreTransformer
    loader: ElasticsearchLoader
    state: ETLState
    
    def run_once(self) -> None:
        changed: ChangedGenres = self.producer.extract(
            genre_checkpoint=self.state.get_checkpoint(
                StateKey.GENRES_GENRE
            ),
            film_work_checkpoint=self.state.get_checkpoint(
                StateKey.GENRES_FILM_WORK
            ),
        )
        
        genres: list[Genre] = self.reader.get_genres(changed.genre_ids)
        
        documents: list[ElasticGenreDocumentModel] = self.transformer.transform_batch(
            genres
        )
        
        self.loader.load(documents)
        
        self.state.set_checkpoint(
            StateKey.GENRES_GENRE,
            changed.genre_checkpoint,
        )
        
        self.state.set_checkpoint(
            StateKey.GENRES_FILM_WORK,
            changed.film_work_checkpoint,
        )
