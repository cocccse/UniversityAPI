from fastapi import APIRouter

from app.major.schemas import MajorAddSchema, MajorUpdateSchema
from app.major.service import MajorService
from app.students.service import StudentService

router = APIRouter(prefix='/majors', tags=['Работа с факультетами'])


@router.post("/add/")
async def register_user(major: MajorAddSchema) -> dict:
    check = await MajorService.add(**major.dict())
    if check:
        return {"message": "Факультет успешно добавлен!", "major": major}
    else:
        return {"message": "Ошибка при добавлении факультета!"}

@router.put("/update_description/")
async def update_major_description(major: MajorUpdateSchema) -> dict:
    check = await MajorService.update(filter_by={'major_name': major.major_name},
                                   major_description=major.major_description)
    if check:
        return {"message": "Описание факультета успешно обновлено!", "major": major}
    else:
        return {"message": "Ошибка при обновлении описания факультета!"}

@router.delete("/delete/{major_id}")
async def delete_major(major_id: int) -> dict:
    check = await MajorService.delete(id=major_id)
    if check:
        return {"message": f"Факультет с ID {major_id} удален!"}
    else:
        return {"message": "Ошибка при удалении факультета!"}

@router.delete("/dell/{student_id}")
async def dell_student_by_id(student_id: int) -> dict:
    check = await StudentService.delete_student_by_id(student_id=student_id)
    if check:
        return {"message": f"Студент с ID {student_id} удален!"}
    else:
        return {"message": "Ошибка при удалении студента!"}