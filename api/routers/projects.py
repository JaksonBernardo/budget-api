from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import (
    CompanyNotFound,
    ClientNotFound,
    ServiceNotFound,
    ProjectNotFound,
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
    ProjectServicePublicSchema,
    ListProjectPublicSchema
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


@project_router.get(
    path = "/{company_id}/{project_id}",
    status_code = status.HTTP_200_OK,
    summary = "Selecionando um projeto especifico",
    response_model = ProjectPublicSchema
)
async def get_project(
    company_id: int,
    project_id: int,
    project_service: ProjectService = Depends(get_project_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:

        project = await project_service.get(company_id, project_id)

        return project

    except (
        CompanyNotFound,
        ProjectNotFound
    ) as e:
        
        raise map_exception(e)


@project_router.get(
    path = "/{company_id}",
    status_code = status.HTTP_200_OK,
    summary = "Listando os projetos por company_id",
    response_model = ListProjectPublicSchema
)
async def list_projects(
    company_id: int,
    limit: int = Query(default = 20, ge = 1, le = 20, description = "Qtd maxima de registro por pagina"),
    offset: int = Query(default = 0, ge = 0, description = "Qtd de registros a serem pulados"),
    client: str = Query(None, description = "Pesquisar pelo cliente do projeto"),
    code: str = Query(None, description = "Pesquisar pelo codigo do projeto"),
    origin: str = Query(None, description = "Pesquisar pelo tipo de origem do projeto"),
    project_service: ProjectService = Depends(get_project_service),
    current_user:  CurrentUser = CurrentUser
):
    
    try:

        pass


    except (CompanyNotFound, ) as e:

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
