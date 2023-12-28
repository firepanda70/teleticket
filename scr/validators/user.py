from scr.core.user import UserDB
from scr.core.validation import ValidationException
from scr.models import User


class UserNotFoundException(ValidationException):
    def __init__(
        self, details: str, http_status_code: int = 404, *args: object
    ) -> None:
        super().__init__(details, http_status_code, *args)


class UserValidator:

    async def check_exists(
        self, user_id: int, user_db: UserDB
    ) -> User:
        db_obj = await user_db.get(id=user_id)
        if not db_obj:
            raise UserNotFoundException(
                f'User with id {user_id} not found'
            )
        return db_obj


user_validator = UserValidator()
