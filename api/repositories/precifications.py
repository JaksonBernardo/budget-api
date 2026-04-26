from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, and_, delete
from sqlalchemy.orm import selectinload
from api.models import (
    Service,
    ServiceMaterial,
    ServiceEmployee,
    ServicePrice
)

class ServiceMaterialRepository:

    def __init__(self, db: AsyncSession):
        self.__db = db

    async def save(self, list_service_material: List[Dict[str, Any]]) -> None:

        query = insert(ServiceMaterial)

        await self.__db.execute(
            query, list_service_material
        )

        await self.__db.flush()
        

class ServiceEmployeeRepository:

    def __init__(self, db: AsyncSession):
        self.__db = db

    async def save(self, list_service_employee: List[Dict[str, Any]]) -> None:

        query = insert(ServiceEmployee)

        await self.__db.execute(
            query, list_service_employee
        )

        await self.__db.flush()
        

class ServicePriceRepository:

    def __init__(self, db: AsyncSession):
        self.__db = db

    async def save(self, list_service_price: List[Dict[str, Any]]) -> None:

        query = insert(ServicePrice)

        await self.__db.execute(
            query, list_service_price
        )

        await self.__db.flush()


class PrecificationServiceRepository:

    def __init__(self, db: AsyncSession):
        self.__db = db


    async def save(self, service: Service) -> Service:

        self.__db.add(service)

        await self.__db.flush()
        await self.__db.refresh(service)

        return service

    async def get_by_name(self, company_id: int, service_name: str) -> Service | None:

        query = select(Service).where(
            and_(
                Service.company_id == company_id,
                Service.name == service_name
            )
        )

        result = await self.__db.execute(query)

        return result.scalar_one_or_none()

    async def get_by_id(self, company_id: int, service_id: int) -> Service:

        query = select(Service).where(
            Service.company_id == company_id,
            Service.id == service_id
        ).options(
            selectinload(Service.materials),
            selectinload(Service.employees),
            selectinload(Service.prices)
        )
        
        result = await self.__db.execute(query)

        return result.scalar_one_or_none()

    async def get_by_company_id(
        self, company_id: int, limit: int, offset: int, search: str | None
    ) -> List[Service]:
        
        query = select(Service).where(Service.company_id == company_id)

        if search:

            query = query.where(
                Service.name.ilike(f"%{search}%")
            )

        query = query.options(
            selectinload(Service.materials),
            selectinload(Service.employees),
            selectinload(Service.prices)
        )

        query = query.limit(limit).offset(offset)

        results = await self.__db.execute(query)

        return results.scalars().all()

    async def delete(self, company_id: int, service_id: int) -> None:

        query = delete(Service).where(
            and_(
                Service.company_id == company_id,
                Service.id == service_id
            )
        )

        await self.__db.execute(query)
        await self.__db.flush()


