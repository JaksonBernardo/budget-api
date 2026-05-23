from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import (
    CompanyNotFound,
    PaymentConditionNotFound,
    PaymentConditionAccesDenied,
    PaymentConditionInvalidName,
    PaymentConditionNameAlreadyExists,
    PaymentConditionAssociatedWithBudget
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import (
    PaymentConditionRepository, 
    CompanyRepository,
    BudgetRepository
)
from api.core.database import get_session
from api.schemas import (
    PaymentConditionSchema,
    PaymentConditionPublicSchema,
    ListPaymentConditionPublicSchema,
    PaymentConditionUpdateSchema
)
from api.services.payment_conditions import PaymentConditionService
from api.security.dependencies import CurrentUser

payment_condition_router = APIRouter(
    prefix = "/api/v1/payment_conditions",
    tags = ["Payment Conditions"]
)

def get_payment_condition_repository(db: AsyncSession = Depends(get_session)) -> PaymentConditionRepository:
    return PaymentConditionRepository(db)

def get_company_repository(db: AsyncSession = Depends(get_session)) -> CompanyRepository:
    return CompanyRepository(db)

def get_budget_repository(db: AsyncSession = Depends(get_session)) -> BudgetRepository:
    return BudgetRepository(db)

def get_payment_condition_service(
    payment_condition_repository: PaymentConditionRepository = Depends(get_payment_condition_repository),
    company_repository: CompanyRepository = Depends(get_company_repository),
    budget_repository: BudgetRepository = Depends(get_budget_repository)
) -> PaymentConditionService:
    return PaymentConditionService(payment_condition_repository, company_repository, budget_repository)


@payment_condition_router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Criando uma condição de pagamento",
    response_model = PaymentConditionPublicSchema
)
async def create_payment_condition(
    payment_condition_data: PaymentConditionSchema,
    service: PaymentConditionService = Depends(get_payment_condition_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        new_payment_condition = await service.create(payment_condition_data)
        return new_payment_condition

    except (CompanyNotFound, PaymentConditionInvalidName, PaymentConditionNameAlreadyExists) as e:
        raise map_exception(e)


@payment_condition_router.get(
    path = "/{company_id}",
    status_code = status.HTTP_200_OK,
    summary = "Listando todas as condições de pagamento",
    response_model = ListPaymentConditionPublicSchema
)
async def list_payment_conditions(
    company_id: int,
    service: PaymentConditionService = Depends(get_payment_condition_service),
    current_user: CurrentUser = CurrentUser,
    offset: int = Query(0, ge = 0, description = "Registros a serem pulados"),
    limit: int = Query(20, ge = 1, le = 100, description = "Qtd máxima de registros apresentados"),
    search: Optional[str] = Query(None, description = "Pesquisar pelo nome de alguma condição de pagamento")
):
    try:
        payment_conditions = await service.list(company_id, offset, limit, search)
        
        return {
            "payment_conditions": payment_conditions,
            "limit": limit,
            "offset": offset
        }

    except CompanyNotFound as e:
        raise map_exception(e)


@payment_condition_router.get(
    path = "/{company_id}/{payment_condition_id}",
    status_code = status.HTTP_200_OK,
    summary = "Selecionando uma condição de pagamento específica",
    response_model = PaymentConditionPublicSchema
)
async def get_payment_condition(
    company_id: int,
    payment_condition_id: int,
    service: PaymentConditionService = Depends(get_payment_condition_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        payment_condition = await service.get(company_id, payment_condition_id)
        return payment_condition

    except (CompanyNotFound, PaymentConditionNotFound) as e:
        raise map_exception(e)


@payment_condition_router.delete(
    path = "/{company_id}/{payment_condition_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Deletando uma condição de pagamento específica"
)
async def delete_payment_condition(
    company_id: int,
    payment_condition_id: int,
    service: PaymentConditionService = Depends(get_payment_condition_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        await service.delete(company_id, payment_condition_id)

    except (CompanyNotFound, PaymentConditionNotFound, PaymentConditionAccesDenied, PaymentConditionAssociatedWithBudget) as e:
        raise map_exception(e)


@payment_condition_router.put(
    path = "/{payment_condition_id}",
    status_code = status.HTTP_200_OK,
    summary = "Atualizando uma condição de pagamento",
    response_model = PaymentConditionPublicSchema
)
async def update_payment_condition(
    payment_condition_id: int,
    payment_condition_data: PaymentConditionUpdateSchema,
    service: PaymentConditionService = Depends(get_payment_condition_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        payment_condition_info = payment_condition_data.model_dump(exclude_unset = True)
        payment_condition = await service.update(payment_condition_id, payment_condition_info)
        return payment_condition

    except (CompanyNotFound, PaymentConditionNotFound, PaymentConditionAccesDenied, PaymentConditionInvalidName, PaymentConditionNameAlreadyExists) as e:
        raise map_exception(e)
