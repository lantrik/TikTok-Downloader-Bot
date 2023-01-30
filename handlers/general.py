import os

from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.ext import keyboards, GetUrl, TikTok
from bot.filters import UrlFilter, CancelFilter



router = Router(name="General Handler")

async def get_url(message: Message) -> None:
    await message.answer(
        "🌀 Wait...",
        reply_markup=keyboards.KeyboardRemove()
    )

    try:
        tik_tok = TikTok(message.text)

        video = tik_tok.download_video(f"{message.from_user.username}.mp4")
        aiovideo = FSInputFile(video)

        await message.answer_video(video=aiovideo)
        os.remove(video)

    except Exception:
        await message.answer("⭕️ The URL is not correct.")

@router.message(Command(commands=["start", "download"]))
async def general_command(message: Message, state: FSMContext) -> None:
    await message.answer(
        "✏️ Enter video URL:",
        reply_markup=keyboards.cancel_keyboard()
    )
    await state.set_state(GetUrl.url)

@router.message(GetUrl.url, CancelFilter(), UrlFilter())
async def get_url_fsm(message: Message, state: FSMContext) -> None:
    await state.update_data(url=message.text)
    await state.clear()

    await get_url(message)

@router.message(UrlFilter())
async def get_url_filter(message: Message) -> None:
    await get_url(message)