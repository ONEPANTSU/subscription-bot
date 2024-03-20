from aiogram import Bot

from src.repositories.repositories import Repositories
from src.services.admin_service import AdminService
from src.services.subscription_service import SubscriptionService


class Services:
    def __init__(self, repositories: Repositories, bot: Bot) -> None:
        self.admin_service = AdminService(repositories.admin_repository)
        self.subscription_service = SubscriptionService(
            repositories.subscription_repository, bot
        )
