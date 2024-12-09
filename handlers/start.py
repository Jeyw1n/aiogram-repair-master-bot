from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from .markups import devices_list_markup


start_router = Router(name=__name__)

MESSAGE_TEXT = '👋 Здравствуйте! Мы готовы помочь вам с ремонтом.\n' \
               'Пожалуйста, выберите устройство, которое нуждается в ' \
               'обслуживании, и мы обработаем ваш запрос.' 


@start_router.message(Command('start'))
async def start_command(msg: Message) -> None:
    await msg.answer(
        text=MESSAGE_TEXT,
        reply_markup=devices_list_markup()
    )