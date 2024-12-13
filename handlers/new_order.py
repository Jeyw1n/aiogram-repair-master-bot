from aiogram import Router, F
from aiogram.types import Message


new_order_router = Router(name=__name__)


@new_order_router.message(F.text == 'Новый заказ 📬')
async def new_order_button_handler(message: Message):
    pass