from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scr.core.db import BaseDBModel


class TicketStatus(StrEnum):
    OPENED = 'opened'
    IN_PROGRESS = 'in_progress'
    CLOSED = 'closed'


class Ticket(BaseDBModel):
    status: Mapped[str]
    tg_user_id: Mapped[int]
    messages: Mapped[list['Message']] = relationship()
    support_user_id: Mapped[int | None] = mapped_column(ForeignKey('user.id'))


class Message(BaseDBModel):
    text: Mapped[str]
    from_client: Mapped[bool]
    ticket_id: Mapped[int] = mapped_column(ForeignKey('ticket.id'))
    support_user_id: Mapped[int | None] = mapped_column(
        ForeignKey('user.id')
    )
