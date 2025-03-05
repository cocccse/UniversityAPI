from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database import async_sessionmaker
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
