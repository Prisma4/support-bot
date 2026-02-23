import asyncio

from celery import shared_task
from celery_worker.app import bot


@shared_task(name="bot.send_message")
def send_message(user_id: int, text: str):
    loop = asyncio.get_event_loop()

    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    coro = bot.send_message(chat_id=user_id, text=text)
    loop.run_until_complete(coro)
