from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base


class Order(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_name: Mapped[str] = mapped_column(unique=True)