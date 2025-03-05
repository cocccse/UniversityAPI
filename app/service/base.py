from fastapi import APIRouter
from sqlalchemy import select

from app.students.models import StudentTable
from app.database import async_sessionmaker

