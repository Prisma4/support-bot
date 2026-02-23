from typing import Optional

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row, Select, ScrollingGroup, Column

from handlers.handlers import switch_state_to_tickets_list, on_select_ticket, tickets_getter, \
    switch_state_to_new_ticket, create_new_ticket, ticket_messages_getter, switch_state_to_new_message, \
    create_new_ticket_message, switch_state_to_main, switch_state_to_view_ticket, create_pagination_handlers
from states import BotStates
from texts import Texts

start_window = Window(
    Const(Texts.WELCOME),
    Button(Const(Texts.NEW_TICKET), id="new_ticket", on_click=switch_state_to_new_ticket),
    Button(Const(Texts.VIEW_TICKETS), id="my_tickets", on_click=switch_state_to_tickets_list),
    state=BotStates.MAIN,
)


def create_pager(
        prefix: str,
        previous_field: Optional[str] = "has_prev",
        next_field: [str] = "has_next"
):
    on_prev, on_next = create_pagination_handlers(prefix)

    pager = Row(
        Button(Format(Texts.PREV), id="prev", on_click=on_prev, when=previous_field),
        Button(Format(Texts.NEXT), id="next", on_click=on_next, when=next_field),
    )

    return pager


ticket_list_window = Window(
    Format(
        f"{Texts.TICKETS_TITLE}\n"
        f"{Texts.TOTAL}: {{count}}\n"
        f"{Texts.PAGE}: {{page}}/{{pages}}\n"
    ),
    Column(
        Select(
            text=Format('⚙️' if "{item.get('is_open')}" else '🔒' "{item[title]}"),
            id="ticket_select",
            items="tickets",
            item_id_getter=lambda item: str(item["id"]),
            on_click=on_select_ticket,
        ),
    ),
    create_pager("tickets_list"),
    Button(Const(Texts.BACK), id="back", on_click=switch_state_to_main),
    state=BotStates.TICKETS_LIST,
    getter=tickets_getter,
)

new_ticket_window = Window(
    Const(Texts.ENTER_TICKET_NAME),
    TextInput(
        id="new_ticket",
        on_success=create_new_ticket,
    ),
    Button(Const(Texts.BACK), id="back", on_click=switch_state_to_main),
    state=BotStates.NEW_TICKET,
)

view_ticket_window = Window(
    Format(
        f"{Texts.TICKET_NAME}: {{name}}\n"
        f"{Texts.MESSAGE_HISTORY}: \n\n"
        f"{{messages}}\n"
        f"{Texts.PAGE}: {{page}}/{{pages}}\n"
    ),
    create_pager("ticket_view"),
    Button(Const(Texts.CLOSE_TICKET), id="close_ticket", on_click=...),
    Button(Const(Texts.NEW_MESSAGE), id="new_message", on_click=switch_state_to_new_message, when="is_open"),
    Button(Const(Texts.BACK), id="back", on_click=switch_state_to_tickets_list),
    state=BotStates.VIEW_TICKET,
    getter=ticket_messages_getter
)

new_message_window = Window(
    Const(Texts.ENTER_MESSAGE_TEXT),
    TextInput(
        id="new_message",
        on_success=create_new_ticket_message
    ),
    Button(Const(Texts.BACK), id="back", on_click=switch_state_to_view_ticket),
    state=BotStates.NEW_MESSAGE,
)

dialog = Dialog(
    start_window,
    ticket_list_window,
    new_ticket_window,
    view_ticket_window,
    new_message_window,
)
