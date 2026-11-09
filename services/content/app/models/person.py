from enum import StrEnum

from sqlalchemy import Column, ForeignKey, String, UniqueConstraint
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base_models import Base, CreatedMixin, ModifiedMixin


class Role(StrEnum):
    ACTOR = "actor"
    DIRECTOR = "director"
    WRITER = "writer"


class PersonModel(Base, CreatedMixin, ModifiedMixin):
    __tablename__ = "person"

    full_name = Column(String(255), nullable=False)

    films = relationship(
        "PersonFilmWorkModel",
        back_populates="person",
        cascade="all, delete-orphan",
    )

    __table_args__ = {"schema": "content"}


class PersonFilmWorkModel(Base, CreatedMixin):
    __tablename__ = "person_film_work"

    person_id = Column(
        UUID(as_uuid=True),
        ForeignKey("content.person.id", ondelete="CASCADE"),
        nullable=False,
    )
    film_work_id = Column(
        UUID(as_uuid=True),
        ForeignKey("content.film_work.id", ondelete="CASCADE"),
        nullable=False,
    )
    role = Column(
        SQLEnum(
            Role,
            native_enum=False,
            create_constraint=False,
            values_callable=lambda enum_cls: [
                item.value for item in enum_cls
            ],
            validate_strings=True,
            length=50,
        ),
        nullable=False,
        default=Role.ACTOR,
    )

    person = relationship("PersonModel", back_populates="films")
    film_work = relationship("FilmModel", back_populates="persons")

    __table_args__ = (
        UniqueConstraint(
            "film_work_id",
            "person_id",
            "role",
            name="pfw_film_person_role_uniq",
        ),
        {"schema": "content"},
    )
