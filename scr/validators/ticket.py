from sqlalchemy.ext.asyncio import AsyncSession

from scr.crud import ticket_crud
from scr.core.validation import ValidationException
from scr.models import TicketStatus, Ticket, User


class OpenedTicketExistsException(ValidationException):
    pass


class LastTiketClosedException(ValidationException):
    pass


class TicketForbiddenException(ValidationException):
    def __init__(
        self, details: str, http_status_code: int = 403, *args: object
    ) -> None:
        super().__init__(details, http_status_code, *args)


class TicketNotFoundException(ValidationException):
    def __init__(
        self, details: str, http_status_code: int = 404, *args: object
    ) -> None:
        super().__init__(details, http_status_code, *args)


class TicketStatusCheckException(ValidationException):
    pass


class TicketValidator:

    async def check_exists(
        self, ticket_id: int, session: AsyncSession
    ) -> Ticket:
        db_obj = await ticket_crud.get_one(ticket_id, session)
        if not db_obj:
            raise TicketNotFoundException(
                f'Ticket with id {ticket_id} not found'
            )
        return db_obj

    async def to_progress_status_check(self, ticket: Ticket) -> bool:
        if ticket.status == TicketStatus.CLOSED:
            raise TicketStatusCheckException(
                'Невозможно взять в работу закрытый тикет'
            )
        if ticket.status == TicketStatus.IN_PROGRESS:
            raise TicketStatusCheckException('Тикет уже взят в работу')
        return True

    async def to_close_status_check(self, ticket: Ticket) -> bool:
        if ticket.status == TicketStatus.CLOSED:
            raise TicketStatusCheckException('Тикет уже закрыт')
        if ticket.status == TicketStatus.OPENED:
            raise TicketStatusCheckException(
                'Нельзя закрыть не взятый в работу тикет'
            )
        return True

    async def check_last_ticket_closed(
        self, tg_user_id: int, session: AsyncSession
    ):
        obj_db = await ticket_crud.get_last_by_tg_user(tg_user_id, session)
        if obj_db is not None and obj_db.status != TicketStatus.CLOSED.value:
            raise OpenedTicketExistsException(
                'Один пользователь может иметь только один не закрытый тикет'
            )
        return True

    async def check_last_ticket_not_closed(
        self, tg_user_id: int, session: AsyncSession
    ):
        obj_db = await ticket_crud.get_last_by_tg_user(tg_user_id, session)
        if obj_db is None or obj_db.status == TicketStatus.CLOSED.value:
            raise LastTiketClosedException(
                'Последний тикет закрыт'
            )
        return obj_db

    async def to_close_rights_check(self, ticket: Ticket, user: User):
        if ticket.support_user_id != user.id:
            raise TicketForbiddenException(
                'Тикет в работе у другого сотрудника'
            )
        return True

    async def reply_to_status_check(self, ticket: Ticket):
        if ticket.status != TicketStatus.IN_PROGRESS.value:
            raise TicketStatusCheckException(
                'Нельзя ответить на тикет не взятый в работу'
            )
        return True

    async def reply_to_rights_check(self, ticket: Ticket, user_id: int):
        if ticket.support_user_id != user_id:
            raise TicketForbiddenException(
                'Тикет в работе у другого сотрудника'
            )
        return True


ticket_validator = TicketValidator()
