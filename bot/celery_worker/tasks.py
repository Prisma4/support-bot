import asyncio
import logging

from aiogram import Bot
from celery import shared_task

from settings import Settings

logger = logging.getLogger(__name__)

settings = Settings()


@shared_task(name="bot.send_message")
def send_message(telegram_id: int, message: str):
    try:
        asyncio.run(_async_send(telegram_id, message))
        logger.info(f"Message sent to {telegram_id}")
    except Exception as e:
        logger.error(f"Error sending to Telegram: {e}", exc_info=True)
        raise


async def _async_send(telegram_id: int, message: str):
    bot = Bot(token=settings.bot_token)
    try:
        await bot.send_message(
            chat_id=telegram_id,
            text=message,
        )
    finally:
        await bot.session.close()
