from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.routers.utils.callbacks.data import (
    ADD_SUBSCRIPTION_DATA,
    REMOVE_SUBSCRIPTION_DATA,
    SUBMIT_ADD_SUBSCRIPTION_DATA,
    SUBMIT_REMOVE_SUBSCRIPTION_DATA,
)
from src.routers.utils.checkers.admin_checker import admin_check, callback_admin_check
from src.routers.utils.filters.buttons_filter import ButtonsFilter
from src.routers.utils.keyboards.admin_keyboards.admin_settings_keyboards import (
    get_admin_keyboard,
)
from src.routers.utils.keyboards.admin_keyboards.subscription_keyboards import (
    get_subscription_settings_inline,
)
from src.routers.utils.keyboards.common_keyboards import get_submit_inline
from src.routers.utils.language.buttons.admin_buttons import get_admin_buttons
from src.routers.utils.language.language_handler import get_language
from src.routers.utils.states.admin_states.add_subscription_state import (
    AddSubscriptionState,
)
from src.services.admin_service import AdminService
from src.services.subscription_service import SubscriptionService


class SubscriptionSettingsRouter(Router):
    def __init__(
        self,
        admin_service: AdminService,
        subscription_service: SubscriptionService,
    ):
        super().__init__(name="admin-router")

        self.admin_service = admin_service
        self.subscription_service = subscription_service

        admin_buttons = get_admin_buttons()

        self.message(ButtonsFilter(admin_buttons["subscription-settings"]))(
            self.subscription_settings
        )
        self.callback_query(F.data.startswith(REMOVE_SUBSCRIPTION_DATA))(
            self.remove_subscription
        )
        self.callback_query(F.data.startswith(SUBMIT_REMOVE_SUBSCRIPTION_DATA))(
            self.remove_subscription_submit
        )
        self.callback_query(F.data == ADD_SUBSCRIPTION_DATA)(self.add_subscription)
        self.message(AddSubscriptionState.set_channel_id)(
            self.add_subscription_set_channel_id
        )
        self.message(AddSubscriptionState.set_link)(self.add_subscription_set_link)
        self.callback_query(F.data.startswith(SUBMIT_ADD_SUBSCRIPTION_DATA))(
            self.add_subscription_submit
        )

    @admin_check
    async def subscription_settings(self, message: Message):
        subscriptions = await self.subscription_service.get_subscriptions()
        lang_text = get_language(message.from_user.language_code)
        await message.answer(
            text=lang_text.messages["subscription-list"],
            reply_markup=get_subscription_settings_inline(
                subscriptions, lang_text.buttons
            ),
        )

    @callback_admin_check
    async def remove_subscription(self, callback: CallbackQuery):
        lang_text = get_language(callback.from_user.language_code)
        subscription_id = callback.data.replace(REMOVE_SUBSCRIPTION_DATA, "")
        subscription = await self.subscription_service.get_subscription(
            int(subscription_id)
        )
        callback_data = SUBMIT_REMOVE_SUBSCRIPTION_DATA + subscription_id + "-"
        await callback.message.answer(
            text=lang_text.messages["remove-subscription-submit"].format(
                channel_id=subscription.channel_id
            ),
            reply_markup=get_submit_inline(
                callback_data=callback_data,
                buttons=lang_text.buttons,
            ),
        )
        await callback.message.delete()

    @callback_admin_check
    async def remove_subscription_submit(self, callback: CallbackQuery):
        lang_text = get_language(callback.from_user.language_code)
        subscription_id, submit = callback.data.replace(
            SUBMIT_REMOVE_SUBSCRIPTION_DATA, ""
        ).split("-")
        subscription = await self.subscription_service.get_subscription(
            int(subscription_id)
        )
        if submit == "yes":
            await self.subscription_service.delete_subscription(subscription.id)
            await callback.message.edit_text(
                text=lang_text.messages["subscription-removed"].format(
                    channel_id=subscription.channel_id
                )
            )
        else:
            await callback.message.edit_text(text=lang_text.messages["cancelled"])

    @callback_admin_check
    async def add_subscription(self, callback: CallbackQuery, state: FSMContext):
        lang_text = get_language(callback.from_user.language_code)
        await callback.message.answer(
            text=lang_text.messages["add-subscription-channel_id"]
        )
        await callback.message.delete()
        await state.set_state(AddSubscriptionState.set_channel_id)

    @admin_check
    async def add_subscription_set_channel_id(
        self, message: Message, state: FSMContext
    ):
        lang_text = get_language(message.from_user.language_code)
        await state.update_data(channel_id=message.text)
        await message.answer(text=lang_text.messages["add-subscription-link"])
        await state.set_state(AddSubscriptionState.set_link)

    @admin_check
    async def add_subscription_set_link(self, message: Message, state: FSMContext):
        lang_text = get_language(message.from_user.language_code)
        await state.update_data(link=message.text)
        state_data = await state.get_data()
        await message.answer(
            text=lang_text.messages["add-subscription-submit"].format(
                channel_id=state_data["channel_id"]
            ),
            reply_markup=get_submit_inline(
                callback_data=SUBMIT_ADD_SUBSCRIPTION_DATA,
                buttons=lang_text.buttons,
            ),
        )

    @callback_admin_check
    async def add_subscription_submit(self, callback: CallbackQuery, state: FSMContext):
        lang_text = get_language(callback.from_user.language_code)
        submit = callback.data.replace(SUBMIT_ADD_SUBSCRIPTION_DATA, "")
        if submit == "yes":
            state_data = await state.get_data()
            await self.subscription_service.create_subscription(
                channel_id=state_data["channel_id"], link=state_data["link"]
            )
            await callback.message.edit_text(
                text=lang_text.messages["subscription-added"].format(
                    channel_id=state_data["channel_id"]
                )
            )
        else:
            await callback.message.edit_text(
                text=lang_text.messages["cancelled"],
            )
        await state.clear()
