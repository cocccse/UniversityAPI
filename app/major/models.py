from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, int_pk, str_uniq


class MajorTable(Base):
    id: Mapped[int_pk]
    major_name: Mapped[str_uniq]
    major_description: Mapped[str | None]
    count_students: Mapped[int] = mapped_column(server_default=text('0'))

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, major_name={self.major_name!r})"

    def __repr__(self):
        return str(self)