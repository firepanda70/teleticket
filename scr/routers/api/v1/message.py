from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from scr.core.db import get_async_session
from scr.models import User
from scr.core.user import current_user
from scr.services.db_services import message_service
from scr.schemas.message import MessagDB, MessageCreate

message_router = APIRouter(prefix='/message', tags=['message'])


@message_router.get(
    '/',
    response_model=list[MessagDB],
    dependencies=[Depends(current_user)],
    response_model_exclude_none=True,
)
async def get_many(
    ticket_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await message_service.get_many(ticket_id, session)


@message_router.post(
    '/',
    response_model=MessagDB
)
async def reply_to_client(
    ticket_id: int,
    message: MessageCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await message_service.create_support_reply(
        ticket_id, message, user, session
    )
