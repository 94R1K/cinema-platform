import time
from dataclasses import dataclass

from .genres.pipeline import GenresPipeline
from .movies.pipeline import MoviesPipeline
from .persons.pipeline import PersonsPipeline


@dataclass
class ETLOrchestrator:
    movies: MoviesPipeline
    persons: PersonsPipeline
    genres: GenresPipeline
    
    def run(self):
        while True:
            self.movies.run_once()
            self.persons.run_once()
            self.genres.run_once()
            time.sleep(1)
