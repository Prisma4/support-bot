import asyncio
import logging

from aiogram import Bot
from celery import shared_task, signals

from settings import Settings

logger = logging.getLogger(__name__)

settings = Settings()


_bot: Bot | None = None


def get_bot() -> Bot:
    global _bot
    if _bot is None:
        _bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        logger.info("Telegram Bot initialized in Celery worker")
    return _bot


@shared_task(name="bot.send_message")
def send_message(telegram_id: int, message: str):
    try:
        asyncio.run(_async_send(telegram_id, message))
        logger.info(f"Message sent to {telegram_id}")
    except Exception as e:
        logger.error(f"Error sending to Telegram: {e}", exc_info=True)
        raise


async def _async_send(telegram_id: int, message: str):
    bot = get_bot()
    await bot.send_message(
        chat_id=telegram_id,
        text=message,
    )


@signals.worker_process_shutdown.connect
def shutdown_bot(**kwargs):
    global _bot
    if _bot is not None:
        try:
            asyncio.run(_bot.session.close())
            logger.info("Telegram Bot session closed on worker shutdown")
        except Exception as e:
            logger.warning(f"Error closing bot session: {e}")
        _bot = None
