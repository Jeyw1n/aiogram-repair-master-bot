from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

DEVICES = {
    'Телефон 📱': 'phone',
    'Ноутбук 💻': 'laptop',
    'Компютер 🖥️': 'computer',
    'Вейп 🚬': 'vape',
    'Другое': 'other'
}


def devices_list_markup() -> InlineKeyboardMarkup:
    """ Returns inline keyboard with devices list """
    buttons = []
    current_row = []
    row_length = 2
    
    for device, callback in DEVICES.items():
        button = InlineKeyboardButton(text=device, callback_data=callback)
        current_row.append(button)
        
        # Adding a row of buttons when the len of row is equal to "row_lenght"
        if len(current_row) == row_length:
            buttons.append(current_row)
            current_row = []
    
    # Add the last row if the rest is empty
    buttons.append(current_row) if current_row is not None else None
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
