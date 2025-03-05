from fastapi import APIRouter, Depends, HTTPException

from app.students.rb import StudentRespModel
from app.students.schemas import StudentSchema
from app.students.service import StudentService

router = APIRouter(prefix='/students', tags=['Студенты'])

@router.get('/', summary='Получить список всех студентов')
async def get_all_students(request_body: StudentRespModel = Depends()) -> list[StudentSchema]:
    return await StudentService.get_all(**request_body.to_dict())

@router.get("/{id}", summary="Получить одного студента по id")
async def get_student_by_id(student_id: int) -> StudentSchema | None:
    result = await StudentService.get_one_or_none_by_id(student_id)
    if result is None:
        raise HTTPException(status_code=404)
    return result

@router.get('/by_filter', summary='Получить одного студента по фильтру')
async def get_student_by_filter(request_body: StudentRespModel = Depends()) -> StudentSchema | dict:
    result = await StudentService.get_one_or_none_by_filter(**request_body.to_dict())
    if result:
        return result
    raise HTTPException(status_code=404)