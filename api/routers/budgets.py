from typing import Optional
from datetime import datetime
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import (
    CompanyNotFound,
    ServiceNotFound,
    ClientNotFound,
    UserNotFound,
    ServicePriceNotFound,
    BudgetNotFound,
    StatusBudgetNotFound,
    PaymentConditionNotFound
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import (
    CompanyRepository,
    PrecificationServiceRepository,
    ClientRepository,
    UserRepository,
    BudgetRepository,
    StatusBudgetRepository,
    BudgetServiceRepository,
    PaymentConditionRepository,
    ProjectRepository,
    ProjectServiceRepository,
    ProjectServiceMaterialRepository
)
from api.core.database import get_session
from api.schemas import (
    BudgetServicesSchema,
    BudgetPublicSchema,
    BudgetSchema,
    BudgetUpdateStatusSchema,
    BudgetUpdateSchema,
    ListBudgetPublicSchema
)
from api.services.budgets import BudgetService
from api.security.dependencies import CurrentUser


budget_router = APIRouter(
    prefix = "/api/v1/budgets",
    tags = ["Budgets"]
)

def get_company_repository(db: AsyncSession = Depends(get_session)) -> CompanyRepository:
    
    return CompanyRepository(db)

def get_precification_repository(db: AsyncSession = Depends(get_session)) -> PrecificationServiceRepository:
    
    return PrecificationServiceRepository(db)

def get_client_repository(db: AsyncSession = Depends(get_session)) -> ClientRepository:

    return ClientRepository(db)

def get_user_repository(db: AsyncSession = Depends(get_session)) -> UserRepository:

    return UserRepository(db)

def get_budget_repository(db: AsyncSession = Depends(get_session)) -> BudgetRepository:

    return BudgetRepository(db)

def get_budget_service_repository(db: AsyncSession = Depends(get_session)) -> BudgetServiceRepository:
    
    return BudgetServiceRepository(db)

def get_status_budget_repository(db: AsyncSession = Depends(get_session)) -> StatusBudgetRepository:

    return StatusBudgetRepository(db)

def get_payment_condition_repository(db: AsyncSession = Depends(get_session)) -> PaymentConditionRepository:

    return PaymentConditionRepository(db)

def get_project_repository(db: AsyncSession = Depends(get_session)) -> ProjectRepository:

    return ProjectRepository(db)

def get_project_service_repository(db: AsyncSession = Depends(get_session)) -> ProjectServiceRepository:

    return ProjectServiceRepository(db)

def get_project_service_material_repository(db: AsyncSession = Depends(get_session)) -> ProjectServiceMaterialRepository:

    return ProjectServiceMaterialRepository(db)

def get_budget_service(
    company_repository: CompanyRepository = Depends(get_company_repository),
    precification_repository: PrecificationServiceRepository = Depends(get_precification_repository),
    client_repository: ClientRepository = Depends(get_client_repository),
    user_repository: UserRepository = Depends(get_user_repository),
    budget_repository: BudgetRepository = Depends(get_budget_repository),
    budget_service_repository: BudgetServiceRepository = Depends(get_budget_service_repository),
    status_budget_repository: StatusBudgetRepository = Depends(get_status_budget_repository),
    payment_condition_repository: PaymentConditionRepository = Depends(get_payment_condition_repository),
    project_repository: ProjectRepository = Depends(get_project_repository),
    project_service_repository: ProjectServiceRepository = Depends(get_project_service_repository),
    project_service_material_repository: ProjectServiceMaterialRepository = Depends(get_project_service_material_repository),
    db: AsyncSession = Depends(get_session)
) -> BudgetService:
    
    return BudgetService(
        company_repository,
        precification_repository,
        client_repository,
        user_repository,
        budget_repository,
        budget_service_repository,
        status_budget_repository,
        payment_condition_repository,
        project_repository,
        project_service_repository,
        project_service_material_repository,
        db
    )


@budget_router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Criando um orcamento",
    response_model = BudgetPublicSchema,
)
async def create(
    budget_data: BudgetSchema,
    budget_service: BudgetService = Depends(get_budget_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:

        budget = await budget_service.create(budget_data)

        return budget
    
    except (
        CompanyNotFound,
        ClientNotFound,
        UserNotFound,
        ServiceNotFound,
        ServicePriceNotFound,
        StatusBudgetNotFound,
        PaymentConditionNotFound
    ) as e:
        
        raise map_exception(e)


@budget_router.get(
    path = "/{company_id}",
    status_code = status.HTTP_200_OK,
    summary = "Listando os orcamentos",
    response_model = ListBudgetPublicSchema
)
async def list_budgets(
    company_id: int,
    budget_service: BudgetService = Depends(get_budget_service),
    current_user: CurrentUser = CurrentUser,
    offset: int = Query(0, ge = 0, description = "Registros a serem pulados"),
    limit: int = Query(20, ge = 1, le = 100, description = "Qtd máxima de registros apresentados"),
    client: Optional[int] = Query(None, description = "Pesquisar pelo ID de algum cliente"),
    user: Optional[int] = Query(None, description = "Usuario que criou o orcamento"),
    year: Optional[int] = Query(datetime.now().year, ge = 1, description = "Pesquisar pelo ano do orcamento"),
    month: Optional[int] = Query(datetime.now().month, ge = 1, le = 12, description = "Pesquisar pelo mes do orcamento")
):
    
    try:

        budgets = await budget_service.list(
            company_id,
            offset,
            limit,
            client,
            user,
            year,
            month
        )

        return {
            "budgets": budgets,
            "limit": limit,
            "offset": offset
        }

    except (CompanyNotFound, ) as e:

        raise map_exception(e)


@budget_router.get(
    path = "/{company_id}/{budget_id}",
    status_code = status.HTTP_200_OK,
    summary = "Selecionando um orcamento especifico",
    response_model = BudgetPublicSchema
)
async def get_budget(
    company_id: int,
    budget_id: int,
    budget_service: BudgetService = Depends(get_budget_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:

        budget = await budget_service.get(company_id, budget_id)

        return budget
    
    except (CompanyNotFound, BudgetNotFound) as e:

        raise map_exception(e)


@budget_router.delete(
    path = "/{company_id}/{budget_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Deletando um orcamento"
)
async def delete(
    company_id: int,
    budget_id: int,
    budget_service: BudgetService = Depends(get_budget_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:

        await budget_service.delete(company_id, budget_id)
    
    except (CompanyNotFound, BudgetNotFound) as e:

        raise map_exception(e)


@budget_router.patch(
    path = "/status/{company_id}/{budget_id}",
    status_code = status.HTTP_200_OK,
    summary = "Atualizando o status de um orcamento",
    response_model = BudgetPublicSchema
)
async def update_status(
    company_id: int,
    budget_id: int,
    data: BudgetUpdateStatusSchema,
    budget_service: BudgetService = Depends(get_budget_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:

        budget = await budget_service.update_status(company_id, budget_id, data)

        return budget

    except (
        CompanyNotFound, 
        BudgetNotFound, 
        StatusBudgetNotFound
    ) as e:

        raise map_exception(e)


@budget_router.put(
    path = "/{company_id}/{budget_id}",
    status_code = status.HTTP_200_OK,
    summary = "Atualizando um orcamento",
    response_model = BudgetPublicSchema
)
async def update(
    company_id: int,
    budget_id: int,
    budget_data: BudgetUpdateSchema,
    budget_service: BudgetService = Depends(get_budget_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:

        budget = await budget_service.update(company_id, budget_id, budget_data)

        return budget
    
    except (
        CompanyNotFound,
        BudgetNotFound,
        ClientNotFound,
        UserNotFound,
        ServiceNotFound,
        ServicePriceNotFound,
        StatusBudgetNotFound,
        PaymentConditionNotFound
    ) as e:

        raise map_exception(e)



