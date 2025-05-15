import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers.dbexec import dbexec_router
from handlers.start import start_router
from handlers.suggestion import suggestions_router

from db.db import init_db

TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise Exception("Null token provided")

async def main():
    dp = Dispatcher()
    dp.include_routers(
        start_router,
        dbexec_router,
        suggestions_router,
    )

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
    asyncio.run(main())
