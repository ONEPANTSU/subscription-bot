import uuid

from src.core.dto.admin import Admin
from src.repositories.admin import AdminAbstractRepository
from src.services.abstract_service import AbstractService


class AdminService(AbstractService):
    repository: AdminAbstractRepository

    def __init__(self, repository: AdminAbstractRepository):
        super().__init__(repository)

    async def check_is_admin(self, username: str) -> bool:
        admins = [admin.username for admin in await self.repository.get_all()]
        return username in admins

    async def get_admin(self, admin_id) -> Admin:
        admin_model = await self.repository.get(admin_id)
        return Admin(**admin_model.get_dict())

    async def get_admins(self) -> list[Admin]:
        admin_models = await self.repository.get_all()
        return [Admin(**admin.get_dict()) for admin in admin_models]

    async def create_admin(self, username: str) -> None:
        await self.repository.create(self.model_table(username=username))

    async def delete_admin(self, admin_id: int | uuid.UUID) -> None:
        await self.repository.delete(admin_id)
