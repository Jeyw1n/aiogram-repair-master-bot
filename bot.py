import os
from dotenv import load_dotenv 

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from database.models import create_connection, create_tables
from handlers import (
    start_router,
    issue_feedback_router,
    new_order_router
)


# Loading a variables from the .env file
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_NAME = "db.sqlite3"


def create_db() -> None:
    db_conn = create_connection(DATABASE_NAME)
    if db_conn is not None:
        create_tables(db_conn)
        db_conn.close()
    else:
        print("Error! cannot create the database connection.")


async def main() -> None:
    create_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        start_router,
        issue_feedback_router,
        new_order_router
    )

    print('Bot started!')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())