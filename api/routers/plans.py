from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import (
    PlanNotFound,
    PlanInvalidName,
    PlanNegativePrice,
    PlanAlreadyExists,
    PlanHaveCompanys
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import (
    PlanRepository,
    CompanyRepository
)
from api.core.database import get_session
from api.schemas import (
    PlanSchema,
    PlanPublicSchema,
    PlanUpdateSchema,
    ListPlanPublicSchema
)
from api.services.plans import PlanService
from api.security.dependencies import CurrentUser


plan_router = APIRouter(
    prefix = "/api/v1/plans",
    tags = ["Plans"]
)

def get_plan_repository(
    db: AsyncSession = Depends(get_session)
) -> PlanRepository:
    
    return PlanRepository(db)

def get_company_repository(
    db: AsyncSession = Depends(get_session)
) -> CompanyRepository:
    
    return CompanyRepository(db)

def get_plan_service(
    plan_repository: PlanRepository = Depends(get_plan_repository)
) -> PlanService:
    
    return PlanService(plan_repository)

@plan_router.post(
    path  = "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Criando um plano de assinatura",
    response_model = PlanPublicSchema
)
async def create_plan(
    plan_data: PlanSchema,
    plan_service: PlanService = Depends(get_plan_service),
    current_user: CurrentUser = CurrentUser
):

    try:

        plan = await plan_service.create(plan_data)

        return plan

    except (PlanInvalidName, PlanNegativePrice, PlanAlreadyExists) as e:

        raise map_exception(e)
    
@plan_router.get(
    path  = "/",
    status_code = status.HTTP_200_OK,
    summary = "Listando os planos da plataforma",
    response_model = ListPlanPublicSchema
)
async def list_plans(
    plan_service: PlanService = Depends(get_plan_service),
    offset: int = Query(0, ge = 0, description = "Registros a serem pulados"),
    limit: int = Query(20, ge = 1, description = "Qtd máxima de registros apresentados"),
    search: Optional[str] = Query(None, description = "Pesquisar pelo nome de algum plano"),
    current_user: CurrentUser = CurrentUser
):

    plans = await plan_service.list_plans(
        limit,
        offset,
        search
    )

    return {
        "plans": plans
    }


@plan_router.get(
    path = "/{plan_id}",
    status_code = status.HTTP_200_OK,
    summary = "Selecionando um plano especifico",
    response_model = PlanPublicSchema
)
async def get_plan(
    plan_id: int,
    plan_service: PlanService = Depends(get_plan_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:

        plan = await plan_service.get_by_id(plan_id)

        return plan

    except PlanNotFound as e:

        raise map_exception(e)


@plan_router.delete(
    path = "/{plan_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Deletando um plano especifico"
)
async def delete_plan(
    plan_id: int,
    plan_service: PlanService = Depends(get_plan_service),
    company_repository: CompanyRepository = Depends(get_company_repository),
    current_user: CurrentUser = CurrentUser
):
    
    try:

        await plan_service.delete_plan(
            company_repository,
            plan_id
        )

    except (PlanHaveCompanys, ) as e:

        raise map_exception(e)


@plan_router.put(
    path = "/{plan_id}",
    status_code = status.HTTP_200_OK,
    summary = "Atualizando um plano",
    response_model = PlanPublicSchema
)
async def update_plan(
    plan_id: int,
    plan_data: PlanUpdateSchema,
    plan_service: PlanService = Depends(get_plan_service),
    current_user: CurrentUser = CurrentUser
):

    try:

        plan_info = plan_data.model_dump(exclude_unset = True)

        new_plan = await plan_service.update_plan(plan_id, plan_info)

        return new_plan

    except (PlanNotFound, PlanInvalidName, PlanNegativePrice) as e:

        raise map_exception(e)



