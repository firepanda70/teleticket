from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import BaseCRUD


class BaseService:
    def __init__(self, crud: BaseCRUD) -> None:
        self.crud = crud

    async def create_one(self, obj_in: BaseModel, session: AsyncSession):
        return await self.crud.create_one(obj_in, session)

    async def get_one(self, obj_id: int, session: AsyncSession):
        return await self.crud.get_one(obj_id, session)

    async def get_many(self, session: AsyncSession):
        return await self.crud.get_many(session)
