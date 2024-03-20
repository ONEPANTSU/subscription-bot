from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src.routers.utils.callbacks.data import CHECK_SUB_DATA


def get_user_keyboard(buttons: dict[str, str]) -> ReplyKeyboardMarkup:
    say_button = KeyboardButton(text=buttons["say"])
    keyboard = [
        [say_button],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_subscribe_checking_keyboard(buttons: dict[str, str]) -> InlineKeyboardMarkup:
    check_button = InlineKeyboardButton(
        text=buttons["check-subscriptions"], callback_data=CHECK_SUB_DATA
    )
    keyboard = [
        [check_button],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
