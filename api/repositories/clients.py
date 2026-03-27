from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
from sqlalchemy.orm import selectinload
from api.models import Client, LegalEntity

class ClientRepository:

    def __init__(self, db: AsyncSession):
        self.__db = db

    async def save(self, client: Client) -> Client:
        self.__db.add(client)
        await self.__db.flush()
        await self.__db.refresh(client)
        return client

    async def get_by_id(self, client_id: int) -> Client | None:
        stmt = select(Client).options(
            selectinload(Client.legal_entity)
        ).where(Client.id == client_id)
        result = await self.__db.execute(stmt)
        return result.scalar_one_or_none()
    
    