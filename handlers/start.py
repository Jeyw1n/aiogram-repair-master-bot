from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

start_router = Router(name=__name__)


@start_router.message(Command('start'))
async def start_command(msg: Message) -> None:
    user_id = msg.from_user.id
    await msg.answer(f'Hi, your id is: {user_id}')