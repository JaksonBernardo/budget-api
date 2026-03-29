from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, delete
from sqlalchemy.orm import selectinload
from api.models import Supplier, LegalEntity

class SupplierRepository:

    def __init__(self, db: AsyncSession):
        self.__db = db

    async def save(self, supplier: Supplier) -> Supplier:
        self.__db.add(supplier)
        await self.__db.flush()
        await self.__db.refresh(supplier)
        return supplier

    async def get_by_id(self, supplier_id: int) -> Supplier | None:

        query = select(Supplier).options(
            selectinload(Supplier.legal_entity)
        ).where(Supplier.id == supplier_id)

        result = await self.__db.execute(query)

        return result.scalar_one_or_none()

    async def get_by_id_and_company(self, company_id: int, supplier_id: int) -> Supplier | None:

        query = select(Supplier).options(
            selectinload(Supplier.legal_entity)
        ).where(
            and_(
                Supplier.id == supplier_id,
                Supplier.company_id == company_id
            )
        )

        result = await self.__db.execute(query)

        return result.scalar_one_or_none()

    async def update(self, supplier: Supplier) -> Supplier:
        try:
            await self.__db.merge(supplier)
            await self.__db.commit()
            await self.__db.refresh(supplier)
            return supplier
        except Exception:
            await self.__db.rollback()
            raise

    async def delete_by_id(self, company_id: int, supplier_id: int) -> None:

        try:
            supplier = await self.get_by_id_and_company(company_id, supplier_id)

            if not supplier:
                return

            legal_entity_id = supplier.legal_entity.id if supplier.legal_entity else None

            query = delete(Supplier).where(
                and_(
                    Supplier.id == supplier_id,
                    Supplier.company_id == company_id
                )
            )

            await self.__db.execute(query)

            if legal_entity_id:
                await self.__db.execute(
                    delete(LegalEntity).where(LegalEntity.id == legal_entity_id)
                )

            await self.__db.commit()
        except Exception:
            await self.__db.rollback()
            raise

    async def get_by_company_id(
        self,
        company_id: int,
        offset: int = 0,
        limit: int = 20,
        search: Optional[str] = None
    ) -> List[Supplier]:

        query = select(Supplier).options(
            selectinload(Supplier.legal_entity)
        ).where(Supplier.company_id == company_id)

        if search:
            query = query.join(LegalEntity).where(
                or_(
                    LegalEntity.companie.ilike(f"%{search}%"),
                    LegalEntity.cpf_cnpj.ilike(f"%{search}%")
                )
            )

        query = query.offset(offset).limit(limit)

        result = await self.__db.execute(query)

        return result.scalars().all()
