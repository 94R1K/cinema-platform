from sqlalchemy import UUID, Column, ForeignKey, String, Text, UniqueConstraint

from .base_models import Base


class GenreModel(Base):
    __tablename__ = "genre"

    name = Column(String(255), nullable=False)
    description = Column(Text(), nullable=True)

    __table_args__ = (
        {"schema": "content"},
    )


class GenreFilmWorkModel(Base):
    __tablename__ = "genre_film_work"

    genre = Column(UUID, ForeignKey("content.genre.uuid"), nullable=False)
    film_work = Column(UUID, ForeignKey("content.film_work.uuid"), nullable=False)

    __table_args__ = (
        UniqueConstraint("film_work", "genre"),
        {"schema": "content"},
    )
