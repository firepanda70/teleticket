from fastapi_users.db import SQLAlchemyBaseUserTable

from scr.core.db import BaseDBModel


class User(SQLAlchemyBaseUserTable[int], BaseDBModel):
    pass
