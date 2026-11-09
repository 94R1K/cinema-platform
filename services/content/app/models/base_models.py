from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )


class CreatedMixin:
    created = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class ModifiedMixin:
    modified = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )