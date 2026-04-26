from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import (
    CompanyNotFound,
    SegmentNotFound,
    PriceNotFound,
    MaterialNotFound,
    EmployeeNotFound,
    PriceExceedValue,
    ServiceNotFound,
    ServiceInvalidName,
    ServiceAccesDenied
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import (
    CompanyRepository,
    SegmentRepository,
    PriceRepository,
    MaterialRepository,
    EmployeeRepository,
    PrecificationServiceRepository,
    ServiceMaterialRepository,
    ServiceEmployeeRepository,
    ServicePriceRepository
)
from api.core.database import get_session
from api.schemas import (
    ServiceSchema,
    ServicePublicSchema,
    ListServicePublicSchema
)
from api.services.precifications import PrecificationService
from api.security.dependencies import CurrentUser

service_router = APIRouter(
    prefix = "/api/v1/services",
    tags = ["Services"]
)

def get_company_repository(db: AsyncSession = Depends(get_session)) -> CompanyRepository:
    return CompanyRepository(db)

def get_segment_repository(db: AsyncSession = Depends(get_session)) -> SegmentRepository:
    return SegmentRepository(db)

def get_material_repository(db: AsyncSession = Depends(get_session)) -> MaterialRepository:
    return MaterialRepository(db)

def get_employee_repository(db: AsyncSession = Depends(get_session)) -> EmployeeRepository:
    return EmployeeRepository(db)

def get_price_repository(db: AsyncSession = Depends(get_session)) -> PriceRepository:
    return PriceRepository(db)

def get_precification_repository(db: AsyncSession = Depends(get_session)) -> PrecificationServiceRepository:
    return PrecificationServiceRepository(db)

def get_service_material_repository(db: AsyncSession = Depends(get_session)) -> ServiceMaterialRepository:
    return ServiceMaterialRepository(db)

def get_service_employee_repository(db: AsyncSession = Depends(get_session)) -> ServiceEmployeeRepository:
    return ServiceEmployeeRepository(db)

def get_service_price_repository(db: AsyncSession = Depends(get_session)) -> ServicePriceRepository:
    return ServicePriceRepository(db)

def get_precification_service(
    segment_repository: SegmentRepository = Depends(get_segment_repository),
    material_repository: MaterialRepository = Depends(get_material_repository),
    employee_repository: EmployeeRepository = Depends(get_employee_repository),
    price_repository: PriceRepository = Depends(get_price_repository),
    precification_repository: PrecificationServiceRepository = Depends(get_precification_repository),
    service_material_repository: ServiceMaterialRepository = Depends(get_service_material_repository),
    service_employee_repository: ServiceEmployeeRepository = Depends(get_service_employee_repository),
    service_price_repository: ServicePriceRepository = Depends(get_service_price_repository),
    company_repository: CompanyRepository = Depends(get_company_repository),
    db: AsyncSession = Depends(get_session)
) -> PrecificationService:
    return PrecificationService(
        segment_repository,
        material_repository,
        employee_repository,
        price_repository,
        precification_repository,
        service_material_repository,
        service_employee_repository,
        service_price_repository,
        company_repository,
        db
    )

@service_router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Criando um serviço",
    response_model = ServicePublicSchema
)
async def create_service(
    service_data: ServiceSchema,
    precification_service: PrecificationService = Depends(get_precification_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        
        new_service = await precification_service.create(service_data)
        return new_service

    except (
        CompanyNotFound, 
        SegmentNotFound, 
        MaterialNotFound, 
        EmployeeNotFound, 
        PriceNotFound,
        PriceExceedValue,
        ServiceInvalidName,
        ServiceAccesDenied
    ) as e:
        raise map_exception(e)


@service_router.get(
    path  = "/{company_id}",
    status_code = status.HTTP_200_OK,
    summary = "Listando os servicos",
    response_model = ListServicePublicSchema
)
async def list_services(
    company_id: int,
    precification_service: PrecificationService = Depends(get_precification_service),
    current_user: CurrentUser = CurrentUser,
    offset: int = Query(0, ge = 0, description = "Registros a serem pulados"),
    limit: int = Query(20, ge = 1, le = 100, description = "Qtd máxima de registros apresentados"),
    search: Optional[str] = Query(None, description = "Pesquisar pelo nome de algum servico")
):
    
    try:

        services = await precification_service.list(
            company_id, limit, offset, search
        )

        return {
            "services": services
        }

    except (CompanyNotFound, ) as e:

        raise map_exception(e)
    

@service_router.get(
    path = "/{company_id}/{service_id}",
    status_code = status.HTTP_200_OK,
    summary = "Selecionando um servico especifico",
    response_model = ServicePublicSchema
)
async def get_service(
    company_id: int,
    service_id: int,
    precification_service: PrecificationService = Depends(get_precification_service),
    current_user: CurrentUser = CurrentUser
):
    
    try:

        service = await precification_service.get(company_id, service_id)

        return service

    except (CompanyNotFound, ServiceNotFound) as e:

        raise map_exception(e)


