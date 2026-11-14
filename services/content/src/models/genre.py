from sqlalchemy import Column, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base_models import Base, CreatedMixin, ModifiedMixin


class GenreModel(Base, CreatedMixin, ModifiedMixin):
    __tablename__ = "genre"

    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    films = relationship(
        "GenreFilmWorkModel",
        back_populates="genre",
        cascade="all, delete-orphan",
    )

    __table_args__ = {"schema": "content"}


class GenreFilmWorkModel(Base, CreatedMixin):
    __tablename__ = "genre_film_work"

    genre_id = Column(
        UUID(as_uuid=True),
        ForeignKey("content.genre.id", ondelete="CASCADE"),
        nullable=False,
    )
    film_work_id = Column(
        UUID(as_uuid=True),
        ForeignKey("content.film_work.id", ondelete="CASCADE"),
        nullable=False,
    )

    genre = relationship("GenreModel", back_populates="films")
    film_work = relationship("FilmModel", back_populates="genres")

    __table_args__ = (
        UniqueConstraint(
            "film_work_id",
            "genre_id",
            name="gfw_film_genre_uniq",
        ),
        {"schema": "content"},
    )
