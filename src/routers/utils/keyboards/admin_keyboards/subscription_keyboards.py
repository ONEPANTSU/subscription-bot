from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.core.dto.subscription import Subscription
from src.routers.utils.callbacks.data import (
    ADD_SUBSCRIPTION_DATA,
    REMOVE_SUBSCRIPTION_DATA,
    SELECT_SUBSCRIPTION_DATA,
)


def get_subscription_settings_inline(
    subscriptions: list[Subscription], buttons: dict[str, str]
) -> InlineKeyboardMarkup:
    keyboard = list()
    for subscription in subscriptions:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=subscription.channel_id,
                    callback_data=f"{SELECT_SUBSCRIPTION_DATA}{subscription.id}",
                ),
                InlineKeyboardButton(
                    text="️❌",
                    callback_data=f"{REMOVE_SUBSCRIPTION_DATA}{subscription.id}",
                ),
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text=buttons["add-subscription"],
                callback_data=ADD_SUBSCRIPTION_DATA,
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
