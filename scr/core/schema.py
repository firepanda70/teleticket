from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class SortMode(StrEnum):
    CREATE_DESC = 'create_desc'
    CREATE_ASC = 'create_asc'
    UPDATE_DESC = 'update_desc'
    UPDATE_ASC = 'update_asc'


class BaseDBSchema(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        from_attributes=True
    )
    id: int
    created_at: datetime
    updated_at: datetime
