from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
from api.models.payment_conditions import PaymentCondition, PaymentInstallment
from sqlalchemy.orm import selectinload

class PaymentConditionRepository:

    def __init__(self, db: AsyncSession):
        self.__db = db

    async def save(self, payment_condition: PaymentCondition) -> PaymentCondition:
        try:
            self.__db.add(payment_condition)
            await self.__db.commit()
            await self.__db.refresh(payment_condition)
            return payment_condition
        except Exception:
            await self.__db.rollback()
            raise

    async def get_by_company_id(
        self, 
        company_id: int, 
        offset: int, 
        limit: int, 
        search: str | None
    ) -> List[PaymentCondition]:
        query = select(PaymentCondition).options(
            selectinload(PaymentCondition.installments)
        ).where(PaymentCondition.company_id == company_id)

        if search:
            query = query.where(PaymentCondition.name.ilike(search))

        query = query.offset(offset).limit(limit)
        
        result = await self.__db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, company_id: int, payment_condition_id: int) -> PaymentCondition | None:
        query = select(PaymentCondition).options(
            selectinload(PaymentCondition.installments)
        ).where(
            and_(
                PaymentCondition.company_id == company_id,
                PaymentCondition.id == payment_condition_id
            )
        )
        result = await self.__db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_name(self, company_id: int, name: str) -> PaymentCondition | None:
        query = select(PaymentCondition).where(
            and_(
                PaymentCondition.company_id == company_id,
                PaymentCondition.name == name
            )
        )
        result = await self.__db.execute(query)
        return result.scalar_one_or_none()

    async def delete_by_id(self, company_id: int, payment_condition_id: int) -> None:
        try:
            await self.__db.execute(
                delete(PaymentCondition).where(
                    and_(
                        PaymentCondition.company_id == company_id,
                        PaymentCondition.id == payment_condition_id
                    )
                )
            )
            await self.__db.commit()
        except Exception:
            await self.__db.rollback()
            raise

    async def update(self, payment_condition: PaymentCondition) -> PaymentCondition:
        try:
            await self.__db.commit()
            await self.__db.refresh(payment_condition)
            return payment_condition
        except Exception:
            await self.__db.rollback()
            raise

    async def delete_installments(self, payment_condition_id: int) -> None:
        try:
            await self.__db.execute(
                delete(PaymentInstallment).where(
                    PaymentInstallment.payment_condition_id == payment_condition_id
                )
            )
            # No commit here, let the service handle it if it's part of a larger transaction
        except Exception:
            await self.__db.rollback()
            raise
