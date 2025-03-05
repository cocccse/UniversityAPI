from sqlalchemy.future import select

from app.database import async_sessionmaker
from app.students.models import StudentTable


class StudentService:
    @classmethod
    async def find_all_students(cls):
        async with async_sessionmaker() as session:
            query = select(StudentTable)
            students = await session.execute(query)
            return students.scalars().all()