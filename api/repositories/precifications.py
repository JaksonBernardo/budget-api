from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
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

    async def get_by_id(self, service_id: int) -> Service:
        query = select(Service).where(
            Service.id == service_id
        ).options(
            selectinload(Service.materials),
            selectinload(Service.employees),
            selectinload(Service.prices)
        )
        
        result = await self.__db.execute(query)
        return result.scalar_one_or_none()


