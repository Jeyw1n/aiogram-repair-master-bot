from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode

from database import Database

get_orders_router = Router(name=__name__)

STATUS_CODES = {
    0: 'На рассмотрении',
    1: 'Выполнен',
    2: 'Отказ'
}


@get_orders_router.message(F.text == 'Список заказов 🗂️')
async def get_orders_button_handler(message: Message):
    """Handler to display a user's orders"""

    user_id = message.from_user.id  # Extract user ID

    try:
        conn = Database()
    
        orders = conn.get_orders(user_id=user_id)  # Fetch user's orders
             
        if not orders:
            await message.answer(
                'У вас пока нет заказов.\n'
                'Создайте новый с помощью кнопки <b>"Новый заказ 📬"</b>.',
                parse_mode=ParseMode.HTML
            )
            return  # Exit if no orders found

        conn.close()
    
    except Exception as ex:
        print(f'Error when getting all orders: {ex}')

    # Build the formatted output string
    for i, order in enumerate(orders, start=1):
        output_text = f'<b>Заказ №{i}:</b>\n'
        output_text += f'<b>Тип устройства:</b> {order.device_type}\n'
        output_text += f'<b>Название:</b> {order.device_name}\n'
        output_text += f'<b>Описание:</b> {order.description}\n'
        output_text += f'<b>Статус:</b> {STATUS_CODES[order.status]}\n'
        output_text += f'<i>Дата создания: {order.created_at}</i>'

        await message.answer(output_text, parse_mode=ParseMode.HTML)