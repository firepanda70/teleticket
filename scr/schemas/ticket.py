from pydantic import BaseModel

from scr.core.schema import BaseDBSchema
from scr.models import TicketStatus


class TicketBase(BaseModel):
    tg_user_id: int


class TicketCreate(TicketBase):
    pass


class TicketDB(BaseDBSchema, TicketBase):
    support_user_id: int | None
    status: TicketStatus
