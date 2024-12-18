from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode

from database import create_connection, get_all_orders
from markups import paginator_markup
import config

admin_router = Router(name=__name__)

PAGE_SIZE = 3  # Number of orders per page


async def generate_page_with_orders(orders_to_display: list) -> str:
    """Generate and send messages with orders."""
    output_text: str = ""
    for order in orders_to_display:
        user_id: int = order.user_id
        try:
            from bot import bot
            user = await bot.get_chat(user_id)
            username = '@' + user.username if user.username else "Нет username"
        except Exception as e:
            print(f"Error getting username for user_id {user_id}: {e}")
            username = "Не удалось получить username"

        output_text += f'<b>Пользователь: {username}</b>\n'
        output_text += f'<b>Тип устройства:</b> {order.device_type}\n'
        output_text += f'<b>Название:</b> {order.device_name}\n'
        output_text += f'<b>Описание:</b> {order.description}\n'
        output_text += f'<i>Дата создания: {order.created_at}</i>\n\n'
    return output_text


@admin_router.message(Command('all'))
async def get_orders_handler(message: Message, page: int = 0) -> None:
    """Outputs all orders as separate messages with pagination."""
    try:
        conn = create_connection(config.DATABASE_NAME)
        orders = get_all_orders(conn=conn)
        conn.close()

        if not orders:
            await message.answer('Пока нет заказов.')
            return

        total_orders: int = len(orders)
        total_pages: int = (total_orders + PAGE_SIZE - 1) // PAGE_SIZE  # Total number of pages

        # Getting orders for the current page
        start_index: int = page * PAGE_SIZE
        end_index: int = start_index + PAGE_SIZE
        orders_to_display: list = orders[start_index:end_index]

        output_text = await generate_page_with_orders(orders_to_display=orders_to_display)
        
        # Отправляем все заказы в одном сообщении
        markup = paginator_markup(page, total_pages)
        await message.answer(
            output_text,
            parse_mode=ParseMode.HTML,
            reply_markup=markup
        )
        
    except Exception as ex:
        print(f'Error when getting orders: {ex}')


@admin_router.callback_query(F.data.startswith('paginator_'))
async def paginator_handler(callback: CallbackQuery) -> None:
    """Handle pagination button clicks."""
    _, page = callback.data.split('_')
    page = int(page)
    
    try:
        conn = create_connection(config.DATABASE_NAME)
        orders = get_all_orders(conn=conn)
        conn.close()

        total_orders: int = len(orders)
        total_pages: int = (total_orders + PAGE_SIZE - 1) // PAGE_SIZE  # Total number of pages

        # Getting orders for the current page
        start_index: int = page * PAGE_SIZE
        end_index: int = start_index + PAGE_SIZE
        orders_to_display: list = orders[start_index:end_index]

        output_text: str = await generate_page_with_orders(orders_to_display=orders_to_display)
    
    except Exception as ex:
        print(f'Error when getting orders: {ex}')
    
    markup = paginator_markup(page, total_pages)
    await callback.message.edit_text(
        text=output_text,
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )
    
    
@admin_router.message(Command('orders'))
async def get_pending_orders_handler(message: Message) -> None:
    pass