from models.genre import ElasticGenreDocumentModel, Genre
from pipelines.common.base_transformer import BaseElasticTransformer


class GenreTransformer(
    BaseElasticTransformer[Genre, ElasticGenreDocumentModel,],
):
    
    def transform(self, genre: Genre) -> ElasticGenreDocumentModel:
        return ElasticGenreDocumentModel(
            index="genres",
            id=genre.id,
            source=Genre(
                id=genre.id,
                name=genre.name,
            ),
        )
