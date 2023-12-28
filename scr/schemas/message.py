from pydantic import BaseModel

from scr.core.schema import BaseDBSchema


class MessageBase(BaseModel):
    text: str


class MessageCreate(MessageBase):
    pass


class MessagDB(BaseDBSchema, MessageBase):
    from_client: bool
    ticket_id: int
    support_user_id: int | None
