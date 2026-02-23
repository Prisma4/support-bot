from api.bot_api import BotApi
from core.api.client import ApiClient
from api.models import PageQuery, PaginatedRetrieveQuery, PaginatedTicketMessages, CreateTicketMessage, \
    PaginatedTickets, \
    CreateTicket, RetrieveQuery, CreatedObject, Ticket

from settings import Settings

settings = Settings()

client = ApiClient(
    base_url=settings.base_api_url,
    headers={
        "X-Telegram-Bot-Api-Token": str(settings.bot_api_token),
    }
)

client.register_endpoint(
    name="get_ticket_messages",
    path="tickets/ticket_messages/list_messages_for_ticket",
    query_validator=PaginatedRetrieveQuery,
    response_validator=PaginatedTicketMessages,
    method="GET"
)
client.register_endpoint(
    name="create_ticket_message",
    path="tickets/ticket_messages/",
    body_validator=CreateTicketMessage,
    method="POST"
)
client.register_endpoint(
    name="get_tickets",
    path="tickets/tickets/",
    query_validator=PageQuery,
    response_validator=PaginatedTickets,
    method="GET"
)
client.register_endpoint(
    name="create_ticket",
    path="tickets/tickets/",
    body_validator=CreateTicket,
    response_validator=CreatedObject,
    method="POST"
)
client.register_endpoint(
    name="get_ticket",
    path="tickets/tickets/",
    query_validator=RetrieveQuery,
    response_validator=Ticket,
    method="POST"
)
client.register_endpoint(
    name="close_ticket",
    path="tickets/tickets/{id}/close_ticket/",
    query_validator=RetrieveQuery,
    method="POST"
)

bot_api = BotApi(client)
