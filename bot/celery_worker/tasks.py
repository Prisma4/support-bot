import asyncio
import logging

from celery import shared_task
from celery_worker.app import bot


logger = logging.getLogger(__name__)


@shared_task(name="bot.send_message")
def send_message(telegram_id, message):
    try:
        asyncio.run(send_telegram_message(telegram_id, message))
    except Exception as e:
        logger.error(f"Error in send_message: {e}")
        raise


async def send_telegram_message(telegram_id, message):
    await bot.send_message(chat_id=telegram_id, text=message)
    logger.info(f"Message sent to {telegram_id}: {message}")
