from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


def main_menu_markup() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text='Новый заказ 📬')
    button_2 = KeyboardButton(text='Список заказов 🗂️')
    button_3 = KeyboardButton(text='О нас 🔍')
    return ReplyKeyboardMarkup(keyboard=[[button_1, button_2], [button_3]], resize_keyboard=True)
