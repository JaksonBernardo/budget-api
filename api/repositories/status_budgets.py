from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
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
    





