from aiogram.filters import BaseFilter
from aiogram.types import Message



class CancelFilter(BaseFilter):
    """Cancel Filter."""
    async def __call__(self, message: Message) -> bool:
        if message.text == "Cancel":
            return False

        return True