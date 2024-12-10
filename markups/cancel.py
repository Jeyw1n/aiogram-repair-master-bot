from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


def cancel_markup() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text='Отмена ❌')
    return ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
