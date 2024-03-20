import functools

from aiogram.types import CallbackQuery, Message

from src.routers.utils.keyboards.user_keyboards.user_keyboards import (
    get_subscribe_checking_keyboard,
)
from src.routers.utils.language.language_handler import get_language


def subscription_check(func):
    @functools.wraps(func)
    async def wrapper(router, message: Message, *args, **kwargs):
        if await router.subscription_service.is_subscribed(message.from_user.id):
            return await func(router, message, *args, **kwargs)
        else:
            await __send_subscribe_claim(router, message)

    return wrapper


def callback_subscription_check(func):
    @functools.wraps(func)
    async def wrapper(router, callback: CallbackQuery, *args, **kwargs):
        message = callback.message
        if await router.subscription_service.is_subscribed(callback.from_user.id):
            return await func(router, callback, *args, **kwargs)
        else:
            await __send_subscribe_claim(router, callback)
            await callback.message.delete()

    return wrapper


async def __send_subscribe_claim(router, event: Message | CallbackQuery):
    lang_text = get_language(event.from_user.language_code)
    text = lang_text.messages["subscribe-start"] + "\n".join(
        await router.subscription_service.get_links()
    )
    message = event if isinstance(event, Message) else event.message
    await message.answer(
        text=text,
        reply_markup=get_subscribe_checking_keyboard(buttons=lang_text.buttons),
    )
