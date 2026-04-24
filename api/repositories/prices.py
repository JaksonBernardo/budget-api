from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete

from api.models import Price

class PriceRepository:

    def __init__(self, db: AsyncSession):
        self.__db = db

    async def save(self, price: Price) -> Price:
        self.__db.add(price)
        await self.__db.commit()
        await self.__db.refresh(price)
        return price

    async def get_by_company_id(
        self,
        company_id: int,
        offset: int,
        limit: int,
        name: str | None = None
    ) -> List[Price]:
        query = select(Price).where(
            Price.company_id == company_id
        )

        if name:
            query = query.where(
                Price.name.ilike(f"%{name}%")
            )

        query = query.offset(offset).limit(limit)

        result = await self.__db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, company_id: int, price_id: int) -> Optional[Price]:
        query = select(Price).where(
            and_(
                Price.id == price_id,
                Price.company_id == company_id
            )
        )

        result = await self.__db.execute(query)
        return result.scalar_one_or_none()

    async def delete_by_id(self, company_id: int, price_id: int) -> None:
        query = delete(Price).where(
            and_(
                Price.id == price_id,
                Price.company_id == company_id
            )
        )

        await self.__db.execute(query)
        await self.__db.commit()

    async def update(self, price: Price) -> Price:
        await self.__db.merge(price)
        await self.__db.commit()
        await self.__db.refresh(price)
        return price
