from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_session
from api.repositories import (
    CompanyRepository,
    PlanRepository,
    SubscriptionRepository
)
from api.schemas import (
    CompanySchema,
    CompanyPublicSchema,
    CompanyUpdateSchema,
    ListCompanyPublicSchema
)
from api.asaas.Asaas import (
    AsaasCustomers,
    AsaasSubscriptions
)
from api.services.companys import CompanyService
from api.security.dependencies import CurrentUser
from api.exceptions.map_exceptions import map_exception
from api.exceptions import (
    CompanyNotFound,
    InvalidNameCompany,
    NameAlreadyExists,
    CnpjAlreadyExists,
    PlanNotFound,
)

company_router = APIRouter(
    prefix="/api/v1/companies",
    tags=["Companies"]
)


def get_company_repository(db: AsyncSession = Depends(get_session)) -> CompanyRepository:

    return CompanyRepository(db)

def get_plan_repository(db: AsyncSession = Depends(get_session)) -> PlanRepository:

    return PlanRepository(db)

def get_subscription_repository(db: AsyncSession = Depends(get_session)) -> SubscriptionRepository:

    return SubscriptionRepository(db)

def get_asaas_customers():

    return AsaasCustomers

def get_asaas_subscriptions():

    return AsaasSubscriptions

def get_company_service(
    company_repository: CompanyRepository = Depends(get_company_repository),
    plan_repository: PlanRepository = Depends(get_plan_repository),
    subscription_repository: SubscriptionRepository = Depends(get_subscription_repository)
) -> CompanyService:
    
    return CompanyService(
        company_repository, 
        plan_repository, 
        subscription_repository
    )


@company_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Assinar plataforma - Criar uma nova empresa",
    response_model=CompanyPublicSchema
)
async def create_company(
    company_data: CompanySchema,
    db: AsyncSession = Depends(get_session),
    asaas_customers: AsaasCustomers = Depends(get_asaas_customers),
    asaas_subscriptions: AsaasCustomers = Depends(get_asaas_subscriptions),
    service: CompanyService = Depends(get_company_service)
):
    
    try:

        new_company = await service.create(
            company_data, 
            asaas_customers,
            asaas_subscriptions
        )
        return new_company
    
    except (PlanNotFound, NameAlreadyExists, CnpjAlreadyExists) as e:

        raise map_exception(e)


@company_router.get(
    path = "/",
    status_code = status.HTTP_200_OK,
    summary = "Listando as empresas assinantes",
    response_model = ListCompanyPublicSchema
)
async def list_companys(
    service: CompanyService = Depends(get_company_service),
    limit: int = Query(10, ge = 1, description = "Qtd maxima de empresas listadas"),
    offset: int  = Query(0, ge = 0, description = "Qtd de registros a serem pulados"),
    search: Optional[str] = Query(None, description = "Pesquisar pelo nome ou CNPJ da empresa"),
    current_user: CurrentUser = CurrentUser
):
    
    companys = await service.list(
        limit, offset, search
    )

    return {
        "companys": companys
    }


@company_router.get(
    path = "/{company_id}",
    status_code = status.HTTP_200_OK,
    summary = "Selecionando uma company especifica",
    response_model = CompanyPublicSchema
)
async def get_company(
    company_id: int,
    service: CompanyService = Depends(get_company_service),
    current_user: CurrentUser = CurrentUser
):

    try:

        company = await service.get_by_id(company_id)

        return company

    except CompanyNotFound as e:

        raise map_exception(e)
    

@company_router.delete(
    path = "/{company_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Deletando um assinante da plataforma"
)
async def delete_company(
    company_id: int,
    service: CompanyService = Depends(get_company_service),
    asaas_customers: AsaasCustomers = Depends(get_asaas_customers),
    asaas_subscriptions: AsaasSubscriptions = Depends(get_asaas_subscriptions),
    current_user: CurrentUser = CurrentUser
):
    
    try:

        await service.delete_company(
            company_id,
            asaas_customers,
            asaas_subscriptions
        )

    except (CompanyNotFound, ) as e:

        raise map_exception(e)


@company_router.put(
    path = "/{company_id}",
    status_code = status.HTTP_200_OK,
    summary = "Atualizando uma company assinante",
    response_model = CompanyPublicSchema
)
async def update_company(
    company_id: int,
    company_data: CompanyUpdateSchema,
    service: CompanyService = Depends(get_company_service),
    asaas_customers: AsaasCustomers = Depends(get_asaas_customers),
    current_user: CurrentUser = CurrentUser
):

    try:

        company_data = company_data.model_dump(exclude_unset = True)

        company = await service.update_company(
            company_data,
            company_id,
            asaas_customers,
        )

        return company


    except (CompanyNotFound, InvalidNameCompany, PlanNotFound) as e:

        raise map_exception(e)


