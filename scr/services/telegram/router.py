from aiogram import Router
from aiogram.types import (
    Message, CallbackQuery, ReplyKeyboardRemove
)
from aiogram.filters import CommandStart

from scr.core.db import AsyncSessionLocal
from scr.services.db_services import ticket_service, message_service
from scr.schemas.ticket import TicketCreate
from scr.validators.ticket import (
    OpenedTicketExistsException, LastTiketClosedException
)
from .messages_const import (
    START_CMD, OPEN_TICKET_MSG,
    TICKET_ALREADY_OPENED_MSG,
    NO_OPENED_TICKET_MSG
)
from .kb import open_ticket_kb

router = Router()


@router.message(CommandStart())
async def process_start_cmd(message: Message):
    await message.reply(
        START_CMD,
        reply_markup=open_ticket_kb
    )


@router.message()
async def process_message(message: Message):
    async with AsyncSessionLocal() as session:
        try:
            await message_service.process_tg_message(
                message, session
            )
        except LastTiketClosedException:
            await message.answer(
                NO_OPENED_TICKET_MSG,
                reply_markup=open_ticket_kb
            )


@router.callback_query(lambda x: x.data == 'open_ticket')
async def process_open_ticket(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.bot.edit_message_reply_markup(
        callback_query.from_user.id,
        callback_query.message.message_id,
        reply_markup=None
    )
    schema = TicketCreate(tg_user_id=callback_query.from_user.id)
    async with AsyncSessionLocal() as session:
        try:
            ticket = await ticket_service.create_one(schema, session)
            text = OPEN_TICKET_MSG.format(ticket.id)
        except OpenedTicketExistsException:
            text = TICKET_ALREADY_OPENED_MSG
    await callback_query.bot.send_message(
        callback_query.from_user.id, text,
        reply_markup=ReplyKeyboardRemove()
    )
