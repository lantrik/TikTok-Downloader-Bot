from aiogram.fsm.context import FSMContext
from aiogram.filters import BaseFilter
from aiogram.types import Message

class CancelFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text == "Отменить":
            return False

        return True