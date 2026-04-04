from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from api.models import Company

class CompanyRepository:

    def __init__(self, db: AsyncSession):

        self.__db = db

    async def get_by_id(self, company_id: int) -> Company | None:

        company = await self.__db.scalar(
            select(Company).where(Company.id == company_id)
        )

        return company
    
    async def verify_if_plan_id(self, plan_id: int) -> bool:

        companys  = await self.__db.execute(
            select(Company).where(Company.plan_id == plan_id)
        )

        return len(companys.scalars().all()) > 0

