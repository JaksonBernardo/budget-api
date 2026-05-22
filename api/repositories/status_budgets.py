from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete, update
from api.models import StatusBudget



class StatusBudgetRepository:


    def __init__(self, db: AsyncSession) -> None:

        self.__db = db


    async def save(self, status_budget: StatusBudget) -> StatusBudget:

        self.__db.add(status_budget)

        await self.__db.flush()
        await self.__db.refresh(status_budget)

        return status_budget


    async def get_by_id(self, company_id: int, status_id: int) -> StatusBudget | None:

        query = select(StatusBudget).where(
            StatusBudget.company_id == company_id,
            StatusBudget.id == status_id
        )

        result = await self.__db.execute(query)

        return result.scalar_one_or_none()
    
    async def get_by_company_id(self, company_id: int, offset: int, limit: int, search: Optional[str] = None) -> List[StatusBudget]:
        
        query = select(StatusBudget).where(
            StatusBudget.company_id == company_id
        )

        if search:
            query = query.where(StatusBudget.name.ilike(f"%{search}%"))

        query = query.offset(offset).limit(limit)
        
        result = await self.__db.execute(query)
        
        return list(result.scalars().all())

    async def get_is_sale_by_company_id(self, company_id: int, exclude_id: int | None = None) -> StatusBudget | None:
        
        query = select(StatusBudget).where(
            and_(
                StatusBudget.company_id == company_id,
                StatusBudget.is_sale == True
            )
        )
        
        if exclude_id:
            query = query.where(StatusBudget.id != exclude_id)
            
        result = await self.__db.execute(query)
        
        return result.scalar_one_or_none()

    async def update(self, company_id: int, status_id: int, data: Dict[str, Any]) -> StatusBudget:
        
        query = update(StatusBudget).where(
            and_(
                StatusBudget.company_id == company_id,
                StatusBudget.id == status_id
            )
        ).values(**data).returning(StatusBudget)
        
        result = await self.__db.execute(query)
        
        return result.scalar_one()

    async def delete(self, company_id: int, status_id: int) -> None:
        
        query = delete(StatusBudget).where(
            and_(
                StatusBudget.company_id == company_id,
                StatusBudget.id == status_id
            )
        )
        
        await self.__db.execute(query)





