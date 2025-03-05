from sqlalchemy import select

from app.database import async_sessionmaker


class BaseService:
    model = None

    @classmethod
    async def get_all(cls, **value):
        async with async_sessionmaker() as session:
            query = select(cls.model).filter_by(**value)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_one_or_none_by_id(cls, data_id: int):
        async with async_sessionmaker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_or_none_by_filter(cls, **filter_by):
        async with async_sessionmaker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()