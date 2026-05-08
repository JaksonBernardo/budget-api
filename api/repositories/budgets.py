from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, and_, delete, update
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


