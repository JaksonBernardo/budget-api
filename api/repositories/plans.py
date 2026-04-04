from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, delete, exists
from sqlalchemy.orm import selectinload
from api.models import Plan

class PlanRepository:

    def __init__(self, db: AsyncSession):
        self.__db = db

    async def create(self, plan: Plan) -> Plan:

        self.__db.add(plan)
        await self.__db.commit()
        await self.__db.refresh(plan)

        return plan
    
    async def verify_exists_by_name(self, plan_name: str) -> Plan | None:

        exists = await self.__db.execute(
            select(Plan).where(Plan.name == plan_name)
        )

        return exists.scalar_one_or_none()

    async def get_all_plans(
        self,
        limit: int,
        offset: int,
        search: str | None
    ) -> List[Plan]:
        
        query = select(Plan)

        if search:

            query = query.where(
                Plan.name.ilike(f"%{search}%")
            )

        query = query.limit(limit).offset(offset)

        plans = await self.__db.execute(query)

        return plans.scalars().all()

    async def get_by_id(self, plan_id: int) -> Plan | None:

        plan = await self.__db.execute(
            select(Plan).where(Plan.id == plan_id)
        )

        return plan.scalar_one_or_none()

    async def delete(self, plan_id: int) -> None:

        await self.__db.execute(
            delete(Plan).where(Plan.id == plan_id)
        )
        await self.__db.commit()

    async def update(self, plan: Plan) -> Plan:

        await self.__db.commit()
        await self.__db.refresh(plan)

        return plan

