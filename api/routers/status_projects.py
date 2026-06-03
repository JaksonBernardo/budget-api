from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import (
    CompanyNotFound,
    StatusProjectNotFound,
    StatusProjectIsCompletedAlreadyExists
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import (
    CompanyRepository,
    StatusProjectRepository
)
from api.core.database import get_session
from api.schemas import (
    StatusProjectSchema,
    StatusProjectPublicSchema,
    StatusProjectUpdateSchema,
    ListStatusProjectPublicSchema
)
from api.services.status_projects import StatusProjectService
from api.security.dependencies import CurrentUser


status_project_router = APIRouter(
    prefix = "/api/v1/status_projects",
    tags = ["Status Projects"]
)

def get_company_repository(db: AsyncSession = Depends(get_session)) -> CompanyRepository:
    
    return CompanyRepository(db)

def get_status_project_repository(db: AsyncSession = Depends(get_session)) -> StatusProjectRepository:

    return StatusProjectRepository(db)

def get_status_project_service(
    company_repository: CompanyRepository = Depends(get_company_repository),
    status_project_repository: StatusProjectRepository = Depends(get_status_project_repository),
    db: AsyncSession = Depends(get_session)
) -> StatusProjectService:
    
    return StatusProjectService(
        company_repository,
        status_project_repository,
        db
    )


@status_project_router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Criando um status de projeto",
    response_model = StatusProjectPublicSchema,
)
async def create(
    status_data: StatusProjectSchema,
    status_project_service: StatusProjectService = Depends(get_status_project_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:
        return await status_project_service.create(status_data)
    
    except (CompanyNotFound, StatusProjectIsCompletedAlreadyExists) as e:
        raise map_exception(e)

@status_project_router.get(
    path = "/{company_id}",
    status_code = status.HTTP_200_OK,
    summary = "Listando os status de projeto",
    response_model = ListStatusProjectPublicSchema
)
async def list_status(
    company_id: int,
    status_project_service: StatusProjectService = Depends(get_status_project_service),
    current_user: CurrentUser = CurrentUser,
    offset: int = Query(0, ge = 0, description = "Registros a serem pulados"),
    limit: int = Query(20, ge = 1, le = 100, description = "Qtd máxima de registros apresentados"),
    search: Optional[str] = Query(None, description = "Pesquisar pelo nome do status")
):
    
    try:

        statuses = await status_project_service.list(company_id, offset, limit, search)

        return {
            "status": statuses,
            "limit": limit,
            "offset": offset
        }

    except (CompanyNotFound) as e:
        raise map_exception(e)


@status_project_router.get(
    path = "/{company_id}/{status_id}",
    status_code = status.HTTP_200_OK,
    summary = "Selecionando um status de projeto especifico",
    response_model = StatusProjectPublicSchema
)
async def get_status(
    company_id: int,
    status_id: int,
    status_project_service: StatusProjectService = Depends(get_status_project_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:

        return await status_project_service.get(company_id, status_id)
    
    except (CompanyNotFound, StatusProjectNotFound) as e:

        raise map_exception(e)


@status_project_router.delete(
    path = "/{company_id}/{status_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Deletando um status de projeto"
)
async def delete(
    company_id: int,
    status_id: int,
    status_project_service: StatusProjectService = Depends(get_status_project_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:
    
        await status_project_service.delete(company_id, status_id)
    
    except (CompanyNotFound, StatusProjectNotFound) as e:

        raise map_exception(e)
    

@status_project_router.put(
    path = "/{company_id}/{status_id}",
    status_code = status.HTTP_200_OK,
    summary = "Atualizando um status de projeto",
    response_model = StatusProjectPublicSchema
)
async def update(
    company_id: int,
    status_id: int,
    status_data: StatusProjectUpdateSchema,
    status_project_service: StatusProjectService = Depends(get_status_project_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:

        return await status_project_service.update(company_id, status_id, status_data)
    
    except (CompanyNotFound, StatusProjectNotFound, StatusProjectIsCompletedAlreadyExists) as e:

        raise map_exception(e)
