from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode

from database import get_orders_by_user_id, create_connection
import config

get_orders_router = Router(name=__name__)


@get_orders_router.message(F.text == 'Список заказов 🗂️')
async def new_order_button_handler(message: Message):
    """Handler to display a user's orders"""

    user_id = message.from_user.id  # Extract user ID

    try:
        conn = create_connection(config.DATABASE_NAME)
    
        orders = get_orders_by_user_id(conn=conn, user_id=user_id)  # Fetch user's orders
             
        if not orders:
            await message.answer(
                'У вас пока нет заказов.\n'
                'Создайте новый с помощью кнопки <b>"Новый заказ 📬"</b>.',
                parse_mode=ParseMode.HTML
            )
            return  # Exit if no orders found

        conn.close()
    
    except Exception as ex:
        print(f'Error when adding an order: {ex}')

    # Build the formatted output string
    for i, order in enumerate(orders, start=1):
        output_text = f'<b>Заказ №{i}:</b>\n'
        output_text += f'<b>Тип устройства:</b> {order.device_type}\n'
        output_text += f'<b>Название:</b> {order.device_name}\n'
        output_text += f'<b>Описание:</b> {order.description}\n'
        output_text += f'<i>Дата создания: {order.created_at}</i>'

        await message.answer(output_text, parse_mode=ParseMode.HTML)