from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from markups import devices_list_markup

new_order_router = Router(name=__name__)

MESSAGE_TEXT = 'Пожалуйста, выберите устройство, которое нуждается в ' \
               'обслуживании, и мы обработаем ваш запрос.' 


@new_order_router.message(F.text == 'Новый заказ 📬')
# @new_order_router.message(Command('new_order'))
async def new_order_button_handler(message: Message):
    await message.answer(
        text=MESSAGE_TEXT,
        reply_markup=devices_list_markup()
    )