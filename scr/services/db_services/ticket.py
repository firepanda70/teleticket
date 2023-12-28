from sqlalchemy.ext.asyncio import AsyncSession

from scr.core.service import BaseService
from scr.core.schema import SortMode
from scr.core.user import UserDB
from scr.crud import ticket_crud
from scr.schemas.ticket import TicketCreate
from scr.models import Ticket, TicketStatus, User
from scr.validators import ticket_validator, user_validator
from scr.services.telegram.bot import (
    send_progress_notification, send_closed_notification
)


class TicketServce(BaseService):

    async def create_one(
        self, obj_in: TicketCreate, session: AsyncSession
    ) -> Ticket:
        await ticket_validator.check_last_ticket_closed(
            obj_in.tg_user_id, session
        )
        return await self.crud.create_one(obj_in, session)

    async def get_many(
        self, status: TicketStatus | None, support_user_id: int | None,
        sort_mode: SortMode | None, user_db: UserDB, session: AsyncSession
    ):
        if support_user_id:
            await user_validator.check_exists(support_user_id, user_db)
        return await ticket_crud.get_many(
            status, support_user_id, sort_mode, session
        )

    async def start_progress(
        self, obj_id: int, user: User, session: AsyncSession
    ) -> Ticket:
        db_obj = await ticket_validator.check_exists(obj_id, session)
        await ticket_validator.to_progress_status_check(db_obj)
        ticket = await ticket_crud.set_in_progress_status(
            db_obj, user.id, session
        )
        await send_progress_notification(
            ticket.tg_user_id, ticket.support_user_id
        )
        return ticket

    async def close_ticket(
        self, obj_id: int, user: User, session: AsyncSession
    ) -> Ticket:
        db_obj = await ticket_validator.check_exists(obj_id, session)
        await ticket_validator.to_close_status_check(db_obj)
        await ticket_validator.to_close_rights_check(db_obj, user)
        ticket = await ticket_crud.set_closed_status(db_obj, session)
        await send_closed_notification(ticket.tg_user_id)
        return ticket


ticket_service = TicketServce(ticket_crud)
