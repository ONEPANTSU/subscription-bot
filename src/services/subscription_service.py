import uuid

from aiogram import Bot
from aiogram.types import Message

from src.core.dto.subscription import Subscription
from src.repositories.subscription import SubscriptionAbstractRepository
from src.services.abstract_service import AbstractService


class SubscriptionService(AbstractService):
    repository: SubscriptionAbstractRepository

    def __init__(self, repository: SubscriptionAbstractRepository, bot: Bot):
        super().__init__(repository)
        self.bot = bot

    async def subscription_claim(self, message: Message) -> bool:
        return await self.is_subscribed(message.from_user.id)

    async def is_subscribed(self, user_id: str) -> bool:
        channels = await self.get_channel_ids()
        is_subscribed = True
        for channel_id in channels:
            chat_member = await self.bot.get_chat_member(channel_id, user_id)
            if chat_member.status not in [
                "member",
                "administrator",
                "creator",
            ]:
                is_subscribed = False
                break
        return is_subscribed

    async def get_links(self):
        channels = await self.get_subscriptions()
        return [channel.link for channel in channels]

    async def get_channel_ids(self):
        channels = await self.get_subscriptions()
        return [channel.channel_id for channel in channels]

    async def get_subscription(self, subscription_id: int) -> Subscription:
        subscription_model = await self.repository.get(subscription_id)
        return Subscription(**subscription_model.get_dict())

    async def get_subscriptions(self) -> list[Subscription]:
        subscription_models = await self.repository.get_all()
        return [Subscription(**admin.get_dict()) for admin in subscription_models]

    async def create_subscription(self, channel_id, link: str) -> None:
        await self.repository.create(self.model_table(channel_id=channel_id, link=link))

    async def delete_subscription(self, subscription_id: int | uuid.UUID) -> None:
        await self.repository.delete(subscription_id)
