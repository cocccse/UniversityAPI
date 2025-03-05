from fastapi import APIRouter

from app.students.service import StudentService

router = APIRouter(prefix='/students', tags=['Студенты'])

@router.get('/', summary='Получить список всех студентов')
async def get_all_students():
    return await StudentService.find_all_students()
