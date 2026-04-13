from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, delete
from api.models import Company

class CompanyRepository:

    def __init__(self, db: AsyncSession):

        self.__db = db

    async def create(self, company: Company) -> Company:

        self.__db.add(company)
        await self.__db.flush()
        await self.__db.refresh(company)

        return company

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

    async def get_all(self, limit: int, offset: int, search: str | None) -> List[Company]:

        query = select(Company)

        if search:

            query = query.where(
                or_(
                    Company.name.ilike(f"%{search}%"),
                    Company.cnpj.ilike(f"%{search}%")
                )
            )

        query = query.limit(limit).offset(offset)

        companys = await self.__db.execute(query)

        return companys.scalars().all()

    async def get_by_name(self, company_name: str) -> Company | None:

        company = await self.__db.execute(
            select(Company).where(Company.name == company_name)
        )

        return company.scalar_one_or_none()
    
    async def get_by_document(self, document: str) -> Company | None:

        """Funcao para coletar a empresa com base no CNPJ ou CPF (Document)"""

        company = await self.__db.execute(
            select(Company).where(Company.cnpj == document)
        )

        return company.scalar_one_or_none()
    
    async def delete(self, company_id: int) -> None:

        await self.__db.execute(
            delete(Company).where(Company.id == company_id)
        )

        await self.__db.commit()

    async def update(self, company: Company) -> Company:

        await self.__db.commit()
        await self.__db.refresh(company)

        return company
