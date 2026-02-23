import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs

from dialogs.dialogs import dialog
from handlers import start
from settings import Settings


logging.basicConfig(level=logging.INFO)

settings = Settings()

bot = Bot(token=settings.bot_token)
dp = Dispatcher()
setup_dialogs(dp)

dp.include_router(dialog)
dp.include_router(start.router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
