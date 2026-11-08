from enum import Enum

from sqlalchemy import Column, Float, Index, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from .base_models import Base


class FilmType(Enum):
    MOVIES = "movies"
    TV_SHOW = "tv show"


class FilmModel(Base):
    __tablename__ = "film_work"

    title = Column(String(255), nullable=False)
    description = Column(Text(), nullable=True)
    rating = Column(Float(), nullable=True)
    type = Column(SQLEnum(FilmType), nullable=False, default=FilmType.MOVIES)
    genres = relationship("GenreFilmWorkModel", backref="film_work")
    persons = relationship("PersonFilmWork", backref="film_work")

    __table_args__ = (
        Index(
            "film_work_creation_rating_idx",
            "creation",
            "rating",
        ),
        {"schema": "content"},
    )
