from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from markups import (
    main_menu_markup
)


start_router = Router(name=__name__)

MESSAGE_TEXT = '👋 *Добро пожаловать!*\n'\
               'Вы попали в бот для оформления заявок на ремонт.\n'\
               'Здесь вы можете быстро и удобно описать вашу проблему, и наш специалист свяжется с вами в ближайшее время.\n\n'\
               'Чтобы создать _новую заявку_, пожалуйста, используйте *меню* внизу.'


@start_router.message(Command('start'))
async def start_command(message: Message) -> None:
    await message.answer(
        text=MESSAGE_TEXT,
        reply_markup=main_menu_markup()
    )