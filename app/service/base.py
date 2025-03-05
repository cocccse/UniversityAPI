from sqlalchemy import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.exc import SQLAlchemyError

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

    @classmethod
    async def update(cls, filter_by, **values):
        async with async_sessionmaker() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(cls.model)
                    .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                    .values(**values)
                    .execution_options(synchronize_session="fetch")
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        if not delete_all and not filter_by:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления.")

        async with async_sessionmaker() as session:
            async with session.begin():
                query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount