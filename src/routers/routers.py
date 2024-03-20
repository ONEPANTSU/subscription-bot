from src.routers.admin_routers.admin_settings_router import AdminSettingsRouter
from src.routers.admin_routers.subscription_settings_router import (
    SubscriptionSettingsRouter,
)
from src.routers.command_router import CommandRouter
from src.routers.user_routers.user_router import UserRouter
from src.services.services import Services


class Routers:

    def __init__(self, services: Services):
        self.command_router = CommandRouter(
            services.admin_service, services.subscription_service
        )
        self.user_router = UserRouter(services.subscription_service)
        self.admin_settings_router = AdminSettingsRouter(services.admin_service)
        self.subscription_settings_router = SubscriptionSettingsRouter(
            services.admin_service, services.subscription_service
        )

    def get_list(self):
        return [
            self.__dict__[router]
            for router in self.__dict__
            if router.endswith("_router")
        ]
