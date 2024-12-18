from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def paginator_markup(current_page: int, page_size: int, total_pages: int) -> InlineKeyboardMarkup:
    """Create an inline keyboard markup for pagination."""
    buttons: list[InlineKeyboardButton] = []
    
    previous_page = current_page - 1
    next_page = current_page + 1
    
    previous_page_callback = f'paginator_{previous_page}_{page_size}'
    next_page_callback = f'paginator_{next_page}_{page_size}'

    previous_page_button = InlineKeyboardButton(text='<', callback_data=previous_page_callback)
    next_page_button = InlineKeyboardButton(text='>', callback_data=next_page_callback)

    if previous_page_button < 0:
        buttons.append(next_page_button)
    elif next_page_button > total_pages:
        buttons.append(previous_page_button)
    else:
        buttons.append(previous_page_button)
        buttons.append(next_page_button)
    
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
