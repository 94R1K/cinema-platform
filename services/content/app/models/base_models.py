from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    uuid = Column(UUID, primary_key=True, default=uuid4)
    creation = Column(DateTime(), default=datetime.now)
    modification = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
