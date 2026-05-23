import pytz
from typing import Dict, List, Optional
from datetime import datetime
from api.models.payment_conditions import PaymentCondition, PaymentInstallment
from api.repositories import PaymentConditionRepository, CompanyRepository, BudgetRepository
from api.schemas.payment_conditions import PaymentConditionSchema
from api.exceptions import (
    CompanyNotFound,
    PaymentConditionNotFound,
    PaymentConditionInvalidName,
    PaymentConditionAccesDenied,
    PaymentConditionNameAlreadyExists,
    PaymentConditionAssociatedWithBudget
)

class PaymentConditionService:

    def __init__(
        self,
        payment_condition_repository: PaymentConditionRepository,
        company_repository: CompanyRepository,
        budget_repository: BudgetRepository
    ):
        self.__payment_condition_repository = payment_condition_repository
        self.__company_repository = company_repository
        self.__budget_repository = budget_repository

    async def create(self, payment_condition_data: PaymentConditionSchema) -> PaymentCondition:
        company = await self.__company_repository.get_by_id(payment_condition_data.company_id)
        if not company:
            raise CompanyNotFound()

        existing = await self.__payment_condition_repository.get_by_name(
            payment_condition_data.company_id, 
            payment_condition_data.name
        )
        if existing:
            raise PaymentConditionNameAlreadyExists()

        payment_condition = PaymentCondition(
            name=payment_condition_data.name,
            billing_type=payment_condition_data.billing_type,
            company_id=payment_condition_data.company_id
        )

        if payment_condition_data.installments:
            payment_condition.installments = [
                PaymentInstallment(
                    order=inst.order,
                    percent=inst.percent,
                    days_after=inst.days_after
                ) for inst in payment_condition_data.installments
            ]

        payment_condition = await self.__payment_condition_repository.save(payment_condition)
        return await self.__payment_condition_repository.get_by_id(
            payment_condition.company_id, 
            payment_condition.id
        )

    async def list(
        self,
        company_id: int,
        offset: int,
        limit: int,
        search: Optional[str]
    ) -> List[PaymentCondition]:
        company = await self.__company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFound()

        if search:
            search = f"%{search}%"

        return await self.__payment_condition_repository.get_by_company_id(
            company_id,
            offset,
            limit,
            search
        )

    async def get(self, company_id: int, payment_condition_id: int) -> PaymentCondition:
        company = await self.__company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFound()

        payment_condition = await self.__payment_condition_repository.get_by_id(company_id, payment_condition_id)
        if not payment_condition:
            raise PaymentConditionNotFound()

        return payment_condition

    async def delete(self, company_id: int, payment_condition_id: int) -> None:
        company = await self.__company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFound()

        payment_condition = await self.__payment_condition_repository.get_by_id(company_id, payment_condition_id)
        if not payment_condition:
            raise PaymentConditionNotFound()
        
        # Check if associated with budgets
        budgets = await self.__budget_repository.get_by_payment_condition(company_id, payment_condition_id)
        if budgets:
            raise PaymentConditionAssociatedWithBudget()

        await self.__payment_condition_repository.delete_by_id(company_id, payment_condition_id)

    async def update(self, payment_condition_id: int, payment_condition_data: Dict) -> PaymentCondition:
        company_id = payment_condition_data.get("company_id")
        company = await self.__company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFound()

        payment_condition = await self.__payment_condition_repository.get_by_id(
            company_id,
            payment_condition_id
        )

        if not payment_condition:
            raise PaymentConditionNotFound()

        if "name" in payment_condition_data:
            if not payment_condition_data["name"]:
                raise PaymentConditionInvalidName()
            
            existing = await self.__payment_condition_repository.get_by_name(
                company_id, 
                payment_condition_data["name"]
            )
            if existing and existing.id != payment_condition_id:
                raise PaymentConditionNameAlreadyExists()
            
            payment_condition.name = payment_condition_data["name"]

        if "billing_type" in payment_condition_data:
            payment_condition.billing_type = payment_condition_data["billing_type"]

        if "installments" in payment_condition_data:
            # Clear old installments and add new ones
            await self.__payment_condition_repository.delete_installments(payment_condition_id)
            payment_condition.installments = [
                PaymentInstallment(
                    order=inst["order"],
                    percent=inst["percent"],
                    days_after=inst["days_after"]
                ) for inst in payment_condition_data["installments"]
            ]

        _BRAZIL_TIMEZONE_ = pytz.timezone("America/Sao_Paulo")
        payment_condition.updated_at = datetime.now(_BRAZIL_TIMEZONE_)

        payment_condition = await self.__payment_condition_repository.update(payment_condition)
        return await self.__payment_condition_repository.get_by_id(
            payment_condition.company_id, 
            payment_condition.id
        )
