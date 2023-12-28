from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from scr.core.crud import BaseCRUD
from scr.models import Message
from scr.schemas.message import MessageCreate


class MessageCRUD(BaseCRUD):
    model: Message

    async def create_one(
            self,
            obj_in: MessageCreate,
            ticket_id: int,
            from_client: bool,
            session: AsyncSession,
            support_user_id: int | None = None
    ):
        if not from_client and support_user_id is None:
            raise ValueError(
                'support_user_id must be defined if message is not from clent'
            )
        elif from_client and support_user_id is not None:
            raise ValueError(
                'support_user_id must not be defined if message is from clent'
            )
        obj_in_data = obj_in.model_dump()
        now = datetime.now()
        obj_in_data['created_at'] = now
        obj_in_data['updated_at'] = now
        obj_in_data['ticket_id'] = ticket_id
        obj_in_data['from_client'] = from_client
        obj_in_data['support_user_id'] = support_user_id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_many(
        self, ticket_id: int, session: AsyncSession
    ) -> list[Message]:
        res = await session.execute(
            select(self.model).where(
                self.model.ticket_id == ticket_id
            ).order_by(self.model.created_at)
        )
        return res.scalars().all()


message_crud = MessageCRUD(Message)
