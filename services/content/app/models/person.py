from enum import Enum

from sqlalchemy import UUID, Column, ForeignKey, String, UniqueConstraint
from sqlalchemy import Enum as SQLEnum

from .base_models import Base


class PersonModel(Base):
    __tablename__ = "person"

    full_name = Column(String(255), nullable=False)

    __table_args__ = (
        {"schema": "content"},
    )


class Role(Enum):
    ACTOR = "actor"
    DIRECTOR = "director"
    WRITER = "writer"


class PersonFilmWorkModel(Base):
    __tablename__ = "person_film_work"

    person = Column(UUID, ForeignKey("content.person.uuid"), nullable=False)
    film_work = Column(UUID, ForeignKey("content.film_work.uuid"), nullable=False)
    role = Column(SQLEnum(Role), nullable=False)

    __table_args__ = (
        UniqueConstraint("film_work", "person", "role"),
        {"schema": "content"},
    )
