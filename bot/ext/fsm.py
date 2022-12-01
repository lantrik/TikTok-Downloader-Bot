from aiogram.fsm.state import StatesGroup, State


class GetUrl(StatesGroup):
    url = State()