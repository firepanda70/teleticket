from datetime import datetime

from sqlalchemy import select, and_ # noqa
from sqlalchemy.ext.asyncio import AsyncSession

from scr.core.schema import SortMode
from scr.core.crud import BaseCRUD
from scr.models import Ticket, TicketStatus
from scr.schemas.ticket import TicketCreate


class TicketCRUD(BaseCRUD):
    model: Ticket

    async def get_last_by_tg_user(
        self,
        tg_user_id: int,
        session: AsyncSession
    ) -> Ticket | None:
        return (await session.execute(
            select(self.model).where(
                self.model.tg_user_id == tg_user_id
            ).order_by(self.model.created_at.desc()))
        ).scalars().first()

    async def create_one(
        self, obj_in: TicketCreate,
        session: AsyncSession
    ) -> Ticket:
        obj_in_data = obj_in.model_dump()
        now = datetime.now()
        obj_in_data['created_at'] = now
        obj_in_data['updated_at'] = now
        obj_in_data['status'] = TicketStatus.OPENED.value
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_many(
        self, status: TicketStatus | None,
        user_id: int | None, sort_mode: SortMode | None,
        session: AsyncSession
    ) -> list[Ticket]:
        query = 'select(self.model).where(and_({0})){1}'
        parts: list[str] = []
        if not status:
            parts.append('self.model.status != TicketStatus.CLOSED.value')
        else:
            parts.append('self.model.status == status.value')
        if user_id:
            parts.append('self.model.support_user_id == user_id')
        if not sort_mode or sort_mode == SortMode.CREATE_ASC:
            order = '.order_by(self.model.created_at)'
        elif sort_mode == SortMode.CREATE_DESC:
            order = '.order_by(self.model.created_at.desc())'
        elif sort_mode == SortMode.UPDATE_ASC:
            order = '.order_by(self.model.updated_at)'
        elif sort_mode == SortMode.UPDATE_DESC:
            order = '.order_by(self.model.updated_at.desc())'
        else:
            raise ValueError('Unexpecded input')
        query = query.format(','.join(parts), order)
        return (await session.execute(eval(query))).scalars().all()

    async def set_in_progress_status(
        self, ticket: Ticket, user_id: int, session: AsyncSession
    ) -> Ticket:
        ticket.status = TicketStatus.IN_PROGRESS.value
        ticket.support_user_id = user_id
        ticket.updated_at = datetime.now()
        session.add(ticket)
        await session.commit()
        await session.refresh(ticket)
        return ticket

    async def set_closed_status(
        self, ticket: Ticket, session: AsyncSession
    ) -> Ticket:
        ticket.status = TicketStatus.CLOSED.value
        ticket.updated_at = datetime.now()
        session.add(ticket)
        await session.commit()
        await session.refresh(ticket)
        return ticket


ticket_crud = TicketCRUD(Ticket)
