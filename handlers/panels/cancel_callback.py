from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext

from bot.ext import keyboards
from ..general import general_command



router = Router(name="General Handler")

@router.message(Command(commands=["cancel"]))
@router.message(Text(text="Cancel"))
async def cancel_command(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return await general_command(message, state)
    
    await state.clear()
    await message.answer(
        "✅ Action canceled.",
        reply_markup=keyboards.KeyboardRemove(),
    )