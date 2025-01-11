from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from database import Database
from handlers import (
    start_router,
    issue_feedback_router,
    new_order_router,
    get_orders_router,
    admin_router,
    update_status_router
)
import config


# Initialize bot and dispatcher
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher(storage=MemoryStorage())


def create_db() -> None:
    """Create database and tables if they do not exist."""
    conn = Database()
    conn.create_tables()
    conn.close()


async def main() -> None:
    create_db()

    dp.include_routers(
        start_router,
        issue_feedback_router,
        new_order_router,
        get_orders_router,
        admin_router,
        update_status_router
    )

    print('Bot started!')
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")