from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode

from database import create_connection, get_all_orders
from markups import paginator_markup
import config

admin_router = Router(name=__name__)

PAGE_SIZE = 3  # Number of orders per page


async def get_username(user_id: int) -> str:
    """Fetch username for a given user_id."""
    try:
        from bot import bot
        user = await bot.get_chat(user_id)
        return f'@{user.username}' if user.username else "Нет username"
    except Exception as e:
        # print(f"Error getting username for user_id {user_id}: {e}")
        return "Не удалось получить username"
    

async def generate_page_with_orders(orders_to_display: list) -> str:
    """Generate and send messages with orders."""
    output_lines = []
    for order in orders_to_display:
        user_id: int = order.user_id
        username = await get_username(user_id=user_id)

        output_lines.append(
            f'<b>ID: {order.order_id}</b>\n'
            f'<b>Пользователь: {username}</b>\n'
            f'<b>Тип устройства:</b> {order.device_type}\n'
            f'<b>Название:</b> {order.device_name}\n'
            f'<b>Описание:</b> {order.description}\n'
            f'<i>Дата создания: {order.created_at}</i>\n'
        )
    return "\n\n".join(output_lines)


async def fetch_orders(page: int) -> tuple[list, int]:
    """Fetch orders and return them along with total count."""
    conn = create_connection(config.DATABASE_NAME)
    orders = get_all_orders(conn=conn)
    conn.close()
    return orders, len(orders)


@admin_router.message(Command('all'))
async def get_orders_handler(message: Message, page: int = 0) -> None:
    """Outputs all orders as separate messages with pagination."""
    orders, total_orders = await fetch_orders(page)
    
    if not orders:
        await message.answer('Пока нет заказов.')
        return

    total_pages: int = (total_orders + PAGE_SIZE - 1) // PAGE_SIZE  # Total number of pages
    orders_to_display: list = orders[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]

    output_text = await generate_page_with_orders(orders_to_display=orders_to_display)
    
    # Sending all orders in one message
    markup = paginator_markup(page, total_pages)
    await message.answer(
        output_text,
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )


@admin_router.callback_query(F.data.startswith('paginator_'))
async def paginator_handler(callback: CallbackQuery) -> None:
    """Handle pagination button clicks."""
    _, page = callback.data.split('_')
    page = int(page)
    
    orders, total_orders = await fetch_orders(page)

    total_pages: int = (total_orders + PAGE_SIZE - 1) // PAGE_SIZE  # Total number of pages
    orders_to_display: list = orders[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]

    output_text: str = await generate_page_with_orders(orders_to_display=orders_to_display)

    markup = paginator_markup(page, total_pages)
    await callback.message.edit_text(
        text=output_text,
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )
    
    
@admin_router.message(Command('orders'))
async def get_pending_orders_handler(message: Message) -> None:
    pass