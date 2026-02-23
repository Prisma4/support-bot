from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select

from api.client import bot_api
from states import BotStates

PAGE_SIZE = 5


async def switch_state_to_tickets(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(BotStates.TICKETS_LIST)


async def on_prev(_: Any, __: Any, manager: DialogManager):
    prev_page = manager.dialog_data.get("prev_page")
    if prev_page:
        manager.dialog_data["page"] = prev_page


async def on_next(_: Any, __: Any, manager: DialogManager):
    next_page = manager.dialog_data.get("next_page")
    if next_page:
        manager.dialog_data["page"] = next_page


async def on_select_ticket(_: Any, __: Any, manager: DialogManager, item_id: str):
    manager.dialog_data["ticket_id"] = int(item_id)


async def tickets_getter(dialog_manager: DialogManager, **_):
    page = int(dialog_manager.dialog_data.get("page", 1))

    user_id = dialog_manager.event.from_user.id

    page = bot_api.get_tickets(user_id, page)

    dialog_manager.dialog_data["prev_page"] = page.previous
    dialog_manager.dialog_data["next_page"] = page.next

    pages = max(1, (page.count + PAGE_SIZE - 1) // PAGE_SIZE)

    return {
        "page": page,
        "pages": pages,
        "count": page.count,
        "has_prev": page.previous is not None,
        "has_next": page.next is not None,
        "tickets": [{"id": t.id, "title": t.name} for t in page.results],
    }
