from typing import Optional, List

from pydantic import BaseModel


class PageQuery(BaseModel):
    page: Optional[int] = None


class RetrieveQuery(BaseModel):
    pk: int


class PaginatedRetrieveQuery(PageQuery, RetrieveQuery):
    pass


class PaginatedPage(BaseModel):
    count: int
    next: int
    previous: int


class User(BaseModel):
    id: int
    username: str
    telegram_user_id: int
    auth_source: str


class TicketMessage(BaseModel):
    id: int
    user: User
    text: str
    ticket: int

    created_at: str


class PaginatedTicketMessages(PaginatedPage):
    results: List[TicketMessage]


class Ticket(BaseModel):
    id: int
    user: User
    processed_by: List[User]
    name: str
    status: int

    created_at: str
    updated_at: str


class PaginatedTickets(PaginatedPage):
    results: List[Ticket]


class CreateTicketMessage(BaseModel):
    text: str
    ticket: int


class CreateTicket(BaseModel):
    name: str
