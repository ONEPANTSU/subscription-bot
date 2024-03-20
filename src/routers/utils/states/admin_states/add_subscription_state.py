from aiogram.fsm.state import State, StatesGroup


class AddSubscriptionState(StatesGroup):
    set_channel_id = State()
    set_link = State()
