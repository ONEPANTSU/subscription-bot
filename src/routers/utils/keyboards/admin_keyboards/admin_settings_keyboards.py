from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src.core.models import Admin
from src.routers.utils.callbacks.data import (
    ADD_ADMIN_DATA,
    REMOVE_ADMIN_DATA,
    SELECT_ADMIN_DATA,
)


def get_admin_keyboard(buttons: dict[str, str]) -> ReplyKeyboardMarkup:
    subscription_settings_button = KeyboardButton(text=buttons["subscription-settings"])
    admins_settings_button = KeyboardButton(text=buttons["admins-settings"])
    keyboard = [[subscription_settings_button], [admins_settings_button]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_admin_settings_inline(
    admins: list[Admin], buttons: dict[str, str]
) -> InlineKeyboardMarkup:
    keyboard = list()
    for admin in admins:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=admin.username,
                    callback_data=f"{SELECT_ADMIN_DATA}{admin.id}",
                ),
                InlineKeyboardButton(
                    text="️❌", callback_data=f"{REMOVE_ADMIN_DATA}{admin.id}"
                ),
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text=buttons["add-admin"], callback_data=ADD_ADMIN_DATA
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
