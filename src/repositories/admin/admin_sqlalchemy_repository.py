from src.core.models import Admin
from src.repositories.admin.admin_abstract_repository import AdminAbstractRepository
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository


class AdminSQLAlchemyRepository(SQLAlchemyRepository, AdminAbstractRepository):
    model_table = Admin
