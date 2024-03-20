from sqlalchemy.orm import Mapped

from src.core.models.annotated_types import int_pk
from src.core.models.base import Base


class Subscription(Base):
    __tablename__ = "subscription"

    id: Mapped[int_pk]
    channel_id: Mapped[str]
    link: Mapped[str]
