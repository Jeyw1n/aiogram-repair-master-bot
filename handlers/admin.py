from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

from database import create_connection, get_all_orders
import config

admin_router = Router(name=__name__)


@admin_router.message(Command('all'))
async def get_orders_handler(message: Message) -> None:
    """Outputs all orders as separate messages"""
    
    try:
        conn = create_connection(config.DATABASE_NAME)
        orders = get_all_orders(conn=conn)
        if not orders:
            await message.answer('Пока нет заказов.')
            return
        conn.close()
    except Exception as ex:
        print(f'Error when getting orders: {ex}')

    # Build the formatted output string
    for order in orders:
        
        user_id = order.user_id
        try:
            from bot import bot

            user = await bot.get_chat(user_id)
            username = '@' + user.username if user.username else "Нет username"
        except Exception as e:
            print(f"Error getting username for user_id {user_id}: {e}")
            username = "Не удалось получить username"


        output_text = f'<b>Пользователь: {username}</b>\n'
        output_text += f'<b>Тип устройства:</b> {order.device_type}\n'
        output_text += f'<b>Название:</b> {order.device_name}\n'
        output_text += f'<b>Описание:</b> {order.description}\n'
        output_text += f'<i>Дата создания: {order.created_at}</i>'

        await message.answer(output_text, parse_mode=ParseMode.HTML)
