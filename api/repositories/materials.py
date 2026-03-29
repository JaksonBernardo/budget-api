from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, and_, or_, delete

from api.models import Material, Supplier, LegalEntity


class MaterialRepository:

    def __init__(self, db: AsyncSession):

        self.__db = db


    async def save(self, material: Material) -> Material:

        self.__db.add(material)
        await self.__db.commit()
        await self.__db.refresh(material)

        return material

    async def get_by_company_id(
        self,
        company_id: int,
        offset: int,
        limit: int,
        name: str | None,
        supplier: str | None
    ) -> List[Material]:

        query = select(Material).where(
            Material.company_id == company_id
        )

        if name:

            query = query.where(
                Material.name.ilike(f"%{name}%")
            )

        if supplier:

            query = query.where(
                Material.supplier.has(
                    Supplier.legal_entity.has(
                        LegalEntity.companie.ilike(f"%{supplier}%")
                    )
                )
            )

        query = query.offset(offset).limit(limit)

        materials = await self.__db.execute(
            query
        )

        return materials.scalars().all()

    async def get_by_id(self, company_id: int, material_id: int) -> Optional[Material]:
        query = select(Material).where(
            and_(
                Material.id == material_id,
                Material.company_id == company_id
            )
        )

        result = await self.__db.execute(query)
        return result.scalar_one_or_none()

    async def delete_by_id(self, company_id: int, material_id: int) -> None:
        query = delete(Material).where(
            and_(
                Material.id == material_id,
                Material.company_id == company_id
            )
        )

        await self.__db.execute(query)
        await self.__db.commit()

    async def update(self, material: Material) -> Material:
        await self.__db.merge(material)
        await self.__db.commit()
        await self.__db.refresh(material)

        return material
    


