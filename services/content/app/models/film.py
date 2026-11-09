from enum import StrEnum

from sqlalchemy import Column, Date, Float, Index, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from .base_models import Base, CreatedMixin, ModifiedMixin


class FilmType(StrEnum):
    MOVIE = "movie"
    TV_SHOW = "tv show"


class FilmModel(Base, CreatedMixin, ModifiedMixin):
    __tablename__ = "film_work"

    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    creation_date = Column(Date, nullable=True)
    rating = Column(Float, nullable=True)

    type = Column(
        SQLEnum(
            FilmType,
            native_enum=False,
            create_constraint=False,
            values_callable=lambda enum_cls: [
                item.value for item in enum_cls
            ],
            validate_strings=True,
            length=20,
        ),
        nullable=False,
        default=FilmType.MOVIE,
    )

    certificate = Column(String(512), nullable=True)
    file_path = Column(String(100), nullable=True)

    genres = relationship(
        "GenreFilmWorkModel",
        back_populates="film_work",
        cascade="all, delete-orphan",
    )
    persons = relationship(
        "PersonFilmWorkModel",
        back_populates="film_work",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("film_work_creation_date_idx", "creation_date"),
        Index("film_work_rating_idx", "rating"),
        {"schema": "content"},
    )
