from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Post(Base, UserRelationMixin):
    _user_back_populates = "posts"
    tittle: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id!r}, tittle={self.tittle!r}, user_id={self.user_id!r})"

    def __repr__(self):
        return str(self)
