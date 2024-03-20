from aiogram.fsm.state import State, StatesGroup


class AddAdminState(StatesGroup):
    set_username = State()
