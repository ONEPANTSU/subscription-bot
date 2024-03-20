from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from src.routers.utils.callbacks.data import CHECK_SUB_DATA
from src.routers.utils.checkers.subscription_checker import (
    callback_subscription_check,
    subscription_check,
)
from src.routers.utils.filters.buttons_filter import ButtonsFilter
from src.routers.utils.keyboards.user_keyboards.user_keyboards import get_user_keyboard
from src.routers.utils.language.buttons.user_buttons import get_user_buttons
from src.routers.utils.language.language_handler import get_language
from src.services.subscription_service import SubscriptionService


class UserRouter(Router):
    def __init__(self, subscription_service: SubscriptionService):
        super().__init__(name="user-router")

        self.subscription_service = subscription_service

        self.callback_query(F.data == CHECK_SUB_DATA)(self.check_subscription)

        user_buttons = get_user_buttons()
        self.message(ButtonsFilter(user_buttons["say"]))(self.say)

    @callback_subscription_check
    async def check_subscription(self, callback: CallbackQuery):
        lang_text = get_language(callback.from_user.language_code)
        await callback.message.answer(
            text=lang_text.messages["user-start"],
            reply_markup=get_user_keyboard(buttons=lang_text.buttons),
        )
        await callback.message.delete()

    @subscription_check
    async def say(self, message: Message):
        lang_text = get_language(message.from_user.language_code)
        await message.answer(lang_text.messages["answer"])
