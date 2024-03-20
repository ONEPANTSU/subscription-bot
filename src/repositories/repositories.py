from src.core.database import DataBase
from src.repositories.admin import AdminSQLAlchemyRepository
from src.repositories.subscription import SubscriptionSQLAlchemyRepository


class Repositories:

    def __init__(self, database: DataBase) -> None:
        self.admin_repository = AdminSQLAlchemyRepository(database)
        self.subscription_repository = SubscriptionSQLAlchemyRepository(database)
