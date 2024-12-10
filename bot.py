import os
from dotenv import load_dotenv 

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from handlers import (
    start_router,
    issue_feedback_router
)


# Loading a variables from the .env file
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        start_router,
        issue_feedback_router
    )

    print('Bot started!')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())