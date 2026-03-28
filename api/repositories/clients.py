from typing import List, Optional
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

        query = select(Client).options(
            selectinload(Client.legal_entity)
        ).where(Client.id == client_id)

        result = await self.__db.execute(query)

        return result.scalar_one_or_none()
    

    async def get_by_company_id(
        self,
        company_id: int,
        offset: int = 0,
        limit: int = 20,
        search: Optional[str] = None
    ) -> List[Client]:

        query = select(Client).options(
            selectinload(Client.legal_entity)
        ).where(Client.company_id == company_id)

        if search:
            query = query.join(LegalEntity).where(
                LegalEntity.companie.ilike(f"%{search}%")
            )

        query = query.offset(offset).limit(limit)

        result = await self.__db.execute(query)

        return result.scalars().all()
    