from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from scr.core.db import get_async_session
from scr.core.user import current_user, UserDB, get_user_db
from scr.core.schema import SortMode
from scr.services.db_services import ticket_service
from scr.schemas.ticket import TicketDB
from scr.models import TicketStatus, User

ticket_router = APIRouter(prefix='/ticket', tags=['ticket'])


@ticket_router.get(
    '/',
    response_model=list[TicketDB],
    dependencies=[Depends(current_user)],
    response_model_exclude_none=True,
)
async def get_many(
    status: TicketStatus | None = None,
    user_id: int | None = None, sort_mode: SortMode | None = None,
    user_db: UserDB = Depends(get_user_db),
    session: AsyncSession = Depends(get_async_session),
):
    return await ticket_service.get_many(
        status, user_id, sort_mode, user_db, session
    )


@ticket_router.post(
    '/{ticket_id}/start_progress',
    response_model=TicketDB,
)
async def start_progress(
        ticket_id: int, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    return await ticket_service.start_progress(ticket_id, user, session)


@ticket_router.post(
    '/{ticket_id}/close',
    response_model=TicketDB
)
async def close_ticket(
    ticket_id: int, user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await ticket_service.close_ticket(ticket_id, user, session)
