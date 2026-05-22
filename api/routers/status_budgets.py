from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import (
    CompanyNotFound,
    StatusBudgetNotFound,
    StatusBudgetIsSaleAlreadyExists
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import (
    CompanyRepository,
    StatusBudgetRepository
)
from api.core.database import get_session
from api.schemas import (
    StatusBudgetSchema,
    StatusBudgetPublicSchema,
    StatusBudgetUpdateSchema,
    ListStatusBudgetPublicSchema
)
from api.services.status_budgets import StatusBudgetService
from api.security.dependencies import CurrentUser


status_budget_router = APIRouter(
    prefix = "/api/v1/status_budgets",
    tags = ["Status Budgets"]
)

def get_company_repository(db: AsyncSession = Depends(get_session)) -> CompanyRepository:
    
    return CompanyRepository(db)

def get_status_budget_repository(db: AsyncSession = Depends(get_session)) -> StatusBudgetRepository:

    return StatusBudgetRepository(db)

def get_status_budget_service(
    company_repository: CompanyRepository = Depends(get_company_repository),
    status_budget_repository: StatusBudgetRepository = Depends(get_status_budget_repository),
    db: AsyncSession = Depends(get_session)
) -> StatusBudgetService:
    
    return StatusBudgetService(
        company_repository,
        status_budget_repository,
        db
    )


@status_budget_router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Criando um status de orcamento",
    response_model = StatusBudgetPublicSchema,
)
async def create(
    status_data: StatusBudgetSchema,
    status_budget_service: StatusBudgetService = Depends(get_status_budget_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:
        return await status_budget_service.create(status_data)
    
    except (CompanyNotFound, StatusBudgetIsSaleAlreadyExists) as e:
        raise map_exception(e)

@status_budget_router.get(
    path = "/{company_id}",
    status_code = status.HTTP_200_OK,
    summary = "Listando os status de orcamento",
    response_model = ListStatusBudgetPublicSchema
)
async def list_status(
    company_id: int,
    status_budget_service: StatusBudgetService = Depends(get_status_budget_service),
    current_user: CurrentUser = CurrentUser,
    offset: int = Query(0, ge = 0, description = "Registros a serem pulados"),
    limit: int = Query(20, ge = 1, le = 100, description = "Qtd máxima de registros apresentados"),
    search: Optional[str] = Query(None, description = "Pesquisar pelo nome do status")
):
    
    try:
        statuses = await status_budget_service.list(company_id, offset, limit, search)
        return {
            "status": statuses,
            "limit": limit,
            "offset": offset
        }

    except (CompanyNotFound) as e:
        raise map_exception(e)


@status_budget_router.get(
    path = "/{company_id}/{status_id}",
    status_code = status.HTTP_200_OK,
    summary = "Selecionando um status de orcamento especifico",
    response_model = StatusBudgetPublicSchema
)
async def get_status(
    company_id: int,
    status_id: int,
    status_budget_service: StatusBudgetService = Depends(get_status_budget_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:
        return await status_budget_service.get(company_id, status_id)
    
    except (CompanyNotFound, StatusBudgetNotFound) as e:
        raise map_exception(e)


@status_budget_router.delete(
    path = "/{company_id}/{status_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Deletando um status de orcamento"
)
async def delete(
    company_id: int,
    status_id: int,
    status_budget_service: StatusBudgetService = Depends(get_status_budget_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:
        await status_budget_service.delete(company_id, status_id)
    
    except (CompanyNotFound, StatusBudgetNotFound) as e:
        raise map_exception(e)
    

@status_budget_router.put(
    path = "/{company_id}/{status_id}",
    status_code = status.HTTP_200_OK,
    summary = "Atualizando um status de orcamento",
    response_model = StatusBudgetPublicSchema
)
async def update(
    company_id: int,
    status_id: int,
    status_data: StatusBudgetUpdateSchema,
    status_budget_service: StatusBudgetService = Depends(get_status_budget_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:
        return await status_budget_service.update(company_id, status_id, status_data)
    
    except (CompanyNotFound, StatusBudgetNotFound) as e:
        raise map_exception(e)
