from aiogram.filters import BaseFilter
from aiogram.types import Message


class UrlFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text.startswith("https://www.tiktok.com/") \
        or message.text.startswith("https://vt.tiktok.com/"):
            return True
        
        await message.answer("⭕️ Кажется, это не является URL-адрессом TikTok.")

        return False
        