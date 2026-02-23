from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select

from api.client import bot_api
from api.models import CreatedObject, PaginatedTickets, PaginatedTicketMessages, Ticket
from core.utils.utils import parse_date
from states import BotStates

PAGE_SIZE = 5


async def switch_state_to_main(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(BotStates.MAIN)


async def switch_state_to_tickets_list(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(BotStates.TICKETS_LIST)


async def switch_state_to_new_ticket(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(BotStates.NEW_TICKET)


async def switch_state_to_new_message(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(BotStates.NEW_MESSAGE)


async def switch_state_to_view_ticket(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(BotStates.TICKET)


async def close_ticket(_: Any, __: Any, manager: DialogManager):
    user_id = manager.event.from_user.id
    ticket_id = manager.dialog_data["ticket_id"]

    response = await bot_api.close_ticket(user_id, ticket_id)

    await manager.switch_to(BotStates.TICKETS_LIST)


async def create_new_ticket(_: Any, __: Any, manager: DialogManager, ticket_name: str):
    ticket_name = ticket_name.strip()
    user_id = manager.event.from_user.id

    response: CreatedObject = await bot_api.create_ticket(user_id, ticket_name)
    ticket_id = response.id
    manager.dialog_data["ticket_id"] = ticket_id

    await manager.switch_to(BotStates.VIEW_TICKET)


async def create_new_ticket_message(_: Any, __: Any, manager: DialogManager, message_text: str):
    message_text = message_text.strip()
    user_id = manager.event.from_user.id

    ticket_id = manager.dialog_data["ticket_id"]

    response: CreatedObject = await bot_api.create_ticket_message(user_id, ticket_id, message_text)

    await manager.switch_to(BotStates.VIEW_TICKET)


def create_pagination_handlers(prefix: str):
    async def on_prev(_, __, manager: DialogManager):
        key = f"{prefix}_page"
        page = int(manager.dialog_data.get(key, 1))
        manager.dialog_data[key] = max(1, page - 1)
        await manager.show()

    async def on_next(_, __, manager: DialogManager):
        key = f"{prefix}_page"
        page = int(manager.dialog_data.get(key, 1))
        manager.dialog_data[key] = page + 1
        await manager.show()

    return on_prev, on_next


async def on_select_ticket(_: Any, __: Any, manager: DialogManager, item_id: str):
    manager.dialog_data["ticket_id"] = int(item_id)
    await manager.switch_to(BotStates.VIEW_TICKET)


async def tickets_getter(dialog_manager: DialogManager, **_):
    page = int(dialog_manager.dialog_data.get("tickets_list_page", 1))

    user_id = dialog_manager.event.from_user.id

    api_page: PaginatedTickets = await bot_api.get_tickets(user_id, page)

    return {
        "page": page,
        "pages": api_page.max_pages,
        "count": api_page.count,
        "has_prev": api_page.previous is not None,
        "has_next": api_page.next is not None,
        "tickets": [t.model_dump() for t in api_page.results],
    }


async def ticket_messages_getter(dialog_manager: DialogManager, **_):
    page = int(dialog_manager.dialog_data.get("ticket_view_page", 1))

    user_id = dialog_manager.event.from_user.id
    ticket_id = dialog_manager.dialog_data["ticket_id"]

    ticket_data: Ticket = await bot_api.get_ticket(user_id, ticket_id)
    messages_api_page: PaginatedTicketMessages = await bot_api.get_ticket_messages(user_id, ticket_id, page)

    user_name = dialog_manager.event.from_user.username

    messages = [
        f"{message.user.username if not message.user.telegram_user_id == user_id else f'@{user_name}'} | {parse_date(message.created_at)}\n"
        f"{message.text}\n"
        for message in messages_api_page.results
    ]

    return {
        "page": page,
        "pages": messages_api_page.max_pages,
        "count": messages_api_page.count,
        "has_prev": messages_api_page.previous is not None,
        "has_next": messages_api_page.next is not None,
        "name": ticket_data.name,
        "is_open": ticket_data.is_open,
        "messages": "\n".join(messages) or "---\n"
    }
