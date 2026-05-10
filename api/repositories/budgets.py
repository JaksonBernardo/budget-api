from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, and_, delete, update, extract
from sqlalchemy.orm import selectinload
from api.models import (
    Budget,
    BudgetService,
)


class BudgetServiceRepository:

    def __init__(self, db: AsyncSession):

        self.__db = db

    async def save(self, list_budget_service: List[Dict[str, Any]]) -> None:

        query = insert(BudgetService)

        await self.__db.execute(
            query, list_budget_service
        )

        await self.__db.flush()


class BudgetRepository:

    def __init__(self, db: AsyncSession):
        
        self.__db = db

    async def save(self, budget: Budget) -> Budget:

        self.__db.add(budget)
        await self.__db.flush()
        await self.__db.refresh(budget)

        return budget

    async def get_by_id(self, company_id: int, budget_id: int) -> Budget | None:

        query = select(Budget).where(
            Budget.company_id == company_id,
            Budget.id == budget_id
        ).options(
            selectinload(Budget.services)
        ).execution_options(populate_existing = True)

        result = await self.__db.execute(query)

        return result.scalar_one_or_none()

    async def get_by_company_id(
        self,
        company_id: int,
        offset: int,
        limit: int,
        client_id: Optional[int] = None,
        user_id: Optional[int] = None,
        year: Optional[int] = datetime.now().year,
        month: Optional[int] = datetime.now().month
    ):
        
        query = select(Budget).where(Budget.company_id == company_id)

        if client_id:

            query = query.where(Budget.client_id == client_id)

        if user_id:

            query = query.where(Budget.user_id == user_id)

        query = query.where(
            extract("month", Budget.created_at) == month,
            extract("year", Budget.created_at) == year
        ).options(
            selectinload(Budget.services)
        ).execution_options(populate_existing = True)

        query = query.limit(limit).offset(offset)

        results = await self.__db.execute(query)

        return results.scalars().all()