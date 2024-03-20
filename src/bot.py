from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from src.core.config.config import Config
from src.core.database import DataBase
from src.repositories.repositories import Repositories
from src.routers.routers import Routers
from src.services.services import Services


async def start_bot():
    config = Config()

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(
            parse_mode=config.bot.parse_mode,
            link_preview_is_disabled=True,
        ),
    )
    dp = Dispatcher(storage=MemoryStorage())

    database = DataBase(config.database)
    repositories = Repositories(database)
    services = Services(repositories, bot)
    routers = Routers(services)

    for router in routers.get_list():
        dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
