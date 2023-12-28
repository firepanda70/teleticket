from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message as TGMessage

from scr.core.service import BaseService
from scr.models import User
from scr.crud import message_crud
from scr.schemas.message import MessageCreate, MessagDB
from scr.validators import ticket_validator
from scr.services.telegram.bot import send_reply


class MessageServce(BaseService):

    async def get_many(self, ticket_id: int, session: AsyncSession):
        await ticket_validator.check_exists(ticket_id, session)
        return await message_crud.get_many(ticket_id, session)

    async def process_tg_message(self, msg: TGMessage, session: AsyncSession):
        ticket = await ticket_validator.check_last_ticket_not_closed(
            msg.from_user.id, session
        )
        schema = MessageCreate(text=msg.text)
        return await message_crud.create_one(schema, ticket.id, True, session)

    async def create_support_reply(
        self, ticket_id: int, data: MessageCreate,
        user: User, session: AsyncSession
    ) -> MessagDB:
        ticket = await ticket_validator.check_exists(ticket_id, session)
        tg_user_id = ticket.tg_user_id
        await ticket_validator.reply_to_status_check(ticket)
        await ticket_validator.reply_to_rights_check(ticket, user.id)
        message = await message_crud.create_one(
            data, ticket_id, False, session, user.id
        )
        await send_reply(tg_user_id, message.text)
        return message


message_service = MessageServce(message_crud)
