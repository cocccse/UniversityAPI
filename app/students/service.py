from sqlalchemy import select, insert, update, event, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.database import async_sessionmaker
from app.major.models import MajorTable
from app.service.base import BaseService
from app.students.models import StudentTable


class StudentService(BaseService):
    model = StudentTable

    @classmethod
    async def find_full_data(cls, student_id: int):
        async with async_sessionmaker() as session:
            # Запрос для получения информации о студенте вместе с информацией о факультете
            query = select(cls.model).options(joinedload(cls.model.major)).filter_by(id=student_id)
            result = await session.execute(query)
            student_info = result.scalar_one_or_none()

            # Если студент не найден, возвращаем None
            if not student_info:
                return None

            student_data = student_info.to_dict()
            student_data['major'] = student_info.major.major_name
            return student_data

    @classmethod
    async def add_student(cls, **student_data: dict):
        async with async_sessionmaker() as session:
            async with session.begin():
                new_student = StudentTable(**student_data)
                session.add(new_student)
                await session.flush()
                new_student_id = new_student.id
                await session.commit()
                return new_student_id

    @event.listens_for(StudentTable, 'after_insert')
    def receive_after_insert(mapper, connection, target):
        major_id = target.major_id
        connection.execute(
            update(MajorTable)
            .where(MajorTable.id == major_id)
            .values(count_students=MajorTable.count_students + 1)
        )

    @event.listens_for(StudentTable, 'after_delete')
    def receive_after_delete(mapper, connection, target):
        major_id = target.major_id
        connection.execute(
            update(MajorTable)
            .where(MajorTable.id == major_id)
            .values(count_students=MajorTable.count_students - 1)
        )

    @classmethod
    async def delete_student_by_id(cls, student_id: int):
        async with async_sessionmaker() as session:
            async with session.begin():
                query = select(cls.model).filter_by(id=student_id)
                result = await session.execute(query)
                student_to_delete = result.scalar_one_or_none()

                if not student_to_delete:
                    return None

                # Удаляем студента
                await session.execute(
                    delete(cls.model).filter_by(id=student_id)
                )

                await session.commit()
                return student_id