from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
from api.models import LegalEntity

class LegalEntityRepository:

    def __init__(self, db: AsyncSession):
        self.__db = db

    async def save(self, legal_entity: LegalEntity) -> LegalEntity:

        self.__db.add(legal_entity)
        await self.__db.flush()
        await self.__db.refresh(legal_entity)
        return legal_entity

    async def get_by_id(self, legal_entity_id: int) -> LegalEntity | None:
        
        result = await self.__db.get(LegalEntity, legal_entity_id)
        return result