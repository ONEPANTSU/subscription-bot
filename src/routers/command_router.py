from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.routers.utils.checkers.subscription_checker import subscription_check
from src.routers.utils.keyboards.admin_keyboards.admin_settings_keyboards import (
    get_admin_keyboard,
)
from src.routers.utils.keyboards.user_keyboards.user_keyboards import get_user_keyboard
from src.routers.utils.language.language_handler import get_language
from src.services.admin_service import AdminService
from src.services.subscription_service import SubscriptionService


class CommandRouter(Router):
    def __init__(
        self,
        admin_service: AdminService,
        subscription_service: SubscriptionService,
    ):
        super().__init__(name="start-router")
        self.admin_service = admin_service
        self.subscription_service = subscription_service
        self.message(Command("start"))(self.start)

    async def start(self, message: Message):
        if await self.admin_service.check_is_admin(message.from_user.username):
            await self.__send_admin_start_message(message)
        else:
            await self.__send_user_start_message(message)

    @staticmethod
    async def __send_admin_start_message(message: Message):
        lang_text = get_language(message.from_user.language_code)
        await message.answer(
            text=lang_text.messages["admin-start"],
            reply_markup=get_admin_keyboard(buttons=lang_text.buttons),
        )

    @subscription_check
    async def __send_user_start_message(self, message: Message):
        lang_text = get_language(message.from_user.language_code)
        await message.answer(
            text=lang_text.messages["user-start"],
            reply_markup=get_user_keyboard(buttons=lang_text.buttons),
        )
