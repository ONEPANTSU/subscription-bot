from sqlalchemy.orm import Mapped

from src.core.models.annotated_types import int_pk
from src.core.models.base import Base


class Admin(Base):
    __tablename__ = "admin"

    id: Mapped[int_pk]
    username: Mapped[str]
