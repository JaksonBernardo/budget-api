from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models import Company

class CompanyRepository:

    def __init__(self, db: AsyncSession):

        self.__db = db

    async def get_by_id(self, company_id: int) -> Company | None:

        company = await self.__db.scalar(
            select(Company).where(Company.id == company_id)
        )

        return company
    

