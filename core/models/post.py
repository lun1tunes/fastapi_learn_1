from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


from .base import Base


class User(Base):
    tittle: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column()
