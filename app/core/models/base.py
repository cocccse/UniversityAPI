from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from core.config import settings
from core.utils.tablename_creator import inflect


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls):
        return inflect.plural(f'{cls.__name__.lower()}')