from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import (
    CompanyNotFound,
    ClientNotFound,
    ServiceNotFound,
    ProjectServiceNotFound
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import (
    CompanyRepository,
    ClientRepository,
    PrecificationServiceRepository,
    ProjectRepository,
    ProjectServiceRepository,
    ProjectServiceMaterialRepository
)
from api.core.database import get_session
from api.schemas import (
    ProjectSchema,
    ProjectPublicSchema,
    ProjectServiceUpdateDeliverySchema,
    ProjectServicePublicSchema
)
from api.services.projects import ProjectService
from api.security.dependencies import CurrentUser


project_router = APIRouter(
    prefix = "/api/v1/projects",
    tags = ["Projects"]
)

def get_company_repository(db: AsyncSession = Depends(get_session)) -> CompanyRepository:
    
    return CompanyRepository(db)

def get_client_repository(db: AsyncSession = Depends(get_session)) -> ClientRepository:

    return ClientRepository(db)

def get_precification_repository(db: AsyncSession = Depends(get_session)) -> PrecificationServiceRepository:
    
    return PrecificationServiceRepository(db)

def get_project_repository(db: AsyncSession = Depends(get_session)) -> ProjectRepository:

    return ProjectRepository(db)

def get_project_service_repository(db: AsyncSession = Depends(get_session)) -> ProjectServiceRepository:
    
    return ProjectServiceRepository(db)

def get_project_service_material_repository(db: AsyncSession = Depends(get_session)) -> ProjectServiceMaterialRepository:
    
    return ProjectServiceMaterialRepository(db)

def get_project_service(
    company_repository: CompanyRepository = Depends(get_company_repository),
    client_repository: ClientRepository = Depends(get_client_repository),
    precification_repository: PrecificationServiceRepository = Depends(get_precification_repository),
    project_repository: ProjectRepository = Depends(get_project_repository),
    project_service_repository: ProjectServiceRepository = Depends(get_project_service_repository),
    project_service_material_repository: ProjectServiceMaterialRepository = Depends(get_project_service_material_repository),
    db: AsyncSession = Depends(get_session)
) -> ProjectService:
    
    return ProjectService(
        company_repository,
        client_repository,
        precification_repository,
        project_repository,
        project_service_repository,
        project_service_material_repository,
        db
    )


@project_router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Criando um projeto",
    response_model = ProjectPublicSchema,
)
async def create(
    project_data: ProjectSchema,
    project_service: ProjectService = Depends(get_project_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:

        project = await project_service.create(project_data)

        return project
    
    except (
        CompanyNotFound,
        ClientNotFound,
        ServiceNotFound
    ) as e:
        
        raise map_exception(e)


@project_router.patch(
    path = "/services/{service_id}/delivery",
    status_code = status.HTTP_200_OK,
    summary = "Atualizando a entrega de um serviço do projeto",
    response_model = ProjectServicePublicSchema
)
async def update_delivery(
    service_id: int,
    delivery_data: ProjectServiceUpdateDeliverySchema,
    project_service: ProjectService = Depends(get_project_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:

        service = await project_service.update_service_delivery(service_id, delivery_data)

        return service
    
    except (ProjectServiceNotFound, ) as e:

        raise map_exception(e)
