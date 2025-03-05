from app.service.base import BaseService
from app.students.models import StudentTable


class StudentService(BaseService):
    model = StudentTable

