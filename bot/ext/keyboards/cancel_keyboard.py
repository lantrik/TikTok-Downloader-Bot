from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



def cancel_keyboard() -> ReplyKeyboardMarkup:
    """
    Undo button.

    Returns
    -------
    :class:`ReplyKeyboardMarkup`
    """
    keyboard_list: List[List[KeyboardButton]] = [
        [KeyboardButton(text="Отменить")]
    ]

    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=keyboard_list,
        resize_keyboard=True,
        input_field_placeholder="Выбрать..."
    )
    return keyboard