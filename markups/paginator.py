from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def paginator_markup(current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    """Create an inline keyboard markup for pagination."""
    buttons: list[InlineKeyboardButton] = []

    # Create previous and next page callbacks
    if current_page > 0:  # If not on the first page
        previous_page_callback = f'paginator_{current_page - 1}'
        previous_page_button = InlineKeyboardButton(text='⏪', callback_data=previous_page_callback)
        buttons.append(previous_page_button)

    if current_page < total_pages - 1:  # If not on the last page
        next_page_callback = f'paginator_{current_page + 1}'
        next_page_button = InlineKeyboardButton(text='⏩', callback_data=next_page_callback)
        buttons.append(next_page_button)

    return InlineKeyboardMarkup(inline_keyboard=[buttons])