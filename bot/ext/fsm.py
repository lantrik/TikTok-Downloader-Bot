from aiogram.fsm.state import StatesGroup, State



class GetUrl(StatesGroup):
    """States group."""
    url = State()