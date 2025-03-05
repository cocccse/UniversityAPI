from sqlalchemy.exc import SQLAlchemyError

from app.database import async_sessionmaker
from app.major.models import MajorTable
from app.service.base import BaseService


class MajorService(BaseService):
    model = MajorTable

    @classmethod
    async def add(cls, **values):
        async with async_sessionmaker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance