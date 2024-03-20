from src.core.models import Subscription
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository
from src.repositories.subscription.subscription_abstract_repository import (
    SubscriptionAbstractRepository,
)


class SubscriptionSQLAlchemyRepository(
    SQLAlchemyRepository, SubscriptionAbstractRepository
):
    model_table = Subscription
