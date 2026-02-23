from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row, Select, ScrollingGroup

from handlers.handlers import switch_state_to_tickets, on_select_ticket, tickets_getter, on_next, on_prev
from states import BotStates
from texts import Texts

start_window = Window(
    Const(Texts.WELCOME),
    Button(Const(Texts.VIEW_TICKETS), id="my_tickets", on_click=switch_state_to_tickets),
    state=BotStates.MAIN,
)

tickets_select = Select(
    text=Format("#{item[id]} {item[title]}"),
    id="ticket_select",
    items="tickets",
    item_id_getter=lambda item: str(item["id"]),
    on_click=on_select_ticket,
)

pager = Row(
    Button(Format(Texts.PREV), id="prev", on_click=on_prev, when="has_prev"),
    Button(Format(Texts.NEXT), id="next", on_click=on_next, when="has_next"),
)

ticket_list_window = Window(
    Format(
        f"{Texts.TICKETS_TITLE}\n"
        f"{Texts.TOTAL}: {{count}}\n"
        f"{Texts.PAGE}: {{page}}/{{pages}}\n"
    ),
    ScrollingGroup(
        tickets_select,
        id="tickets_scroll",
        width=1,
        height=5,
    ),
    pager,
    state=BotStates.TICKETS_LIST,
    getter=tickets_getter,
)

dialog = Dialog(start_window, ticket_list_window)