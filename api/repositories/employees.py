from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
from api.models.employees import Employee

class EmployeeRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db

    async def save(self, employee: Employee) -> Employee:
        try:
            self.__db.add(employee)
            await self.__db.commit()
            await self.__db.refresh(employee)
            return employee
        except Exception:
            await self.__db.rollback()
            raise

    async def get_by_company_id(
        self, 
        company_id: int, 
        offset: int, 
        limit: int, 
        search: Optional[str]
    ) -> List[Employee]:
        query = select(Employee).where(Employee.company_id == company_id)
        if search:
            query = query.where(Employee.name.ilike(search))
        
        query = query.offset(offset).limit(limit)
        result = await self.__db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, company_id: int, employee_id: int) -> Optional[Employee]:
        query = select(Employee).where(
            and_(
                Employee.company_id == company_id,
                Employee.id == employee_id
            )
        )
        result = await self.__db.execute(query)
        return result.scalar_one_or_none()

    async def delete_by_id(self, company_id: int, employee_id: int) -> None:
        try:
            await self.__db.execute(
                delete(Employee).where(
                    and_(
                        Employee.company_id == company_id,
                        Employee.id == employee_id
                    )
                )
            )
            await self.__db.commit()
        except Exception:
            await self.__db.rollback()
            raise

    async def update(self, employee: Employee) -> Employee:
        try:
            await self.__db.commit()
            await self.__db.refresh(employee)
            return employee
        except Exception:
            await self.__db.rollback()
            raise
