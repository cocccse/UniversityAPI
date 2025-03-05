from app.major.models import MajorTable
from app.service.base import BaseService


class MajorsService(BaseService):
    model = MajorTable