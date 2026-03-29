from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import (
    CompanyNotFound,
    MaterialInvalidName,
    MaterialNotFound,
    SupplierNotFound
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import (
    MaterialRepository,
    SupplierRepository, 
    CompanyRepository
)
from api.core.database import get_session
from api.schemas import (
    MaterialSchema,
    MaterialPublicSchema,
    MaterialUpdateSchema,
    ListMaterialPublicSchema
)
from api.services.materials.service import MaterialService


material_router = APIRouter(
    prefix = "/api/materials",
    tags = ["Materials"]
)


def get_material_repository(
    db: AsyncSession = Depends(get_session)
) -> MaterialRepository:
    
    return MaterialRepository(db)

def get_supplier_repository(
    db: AsyncSession = Depends(get_session)
) -> SupplierRepository:
    
    return SupplierRepository(db)

def get_company_repository(
    db: AsyncSession = Depends(get_session)
) -> CompanyRepository:
    
    return CompanyRepository(db)

def get_material_service(
    material_repository: MaterialRepository = Depends(get_material_repository),
    supplier_repository: MaterialRepository = Depends(get_supplier_repository),
    company_repository: MaterialRepository = Depends(get_company_repository),
) -> MaterialService:
    
    return MaterialService(
        material_repository,
        supplier_repository,
        company_repository
    )


@material_router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Criando um material",
    response_model = MaterialPublicSchema
)
async def create_material(
    material_data: MaterialSchema,
    material_service: MaterialService = Depends(get_material_service)
):
    
    try:

        material = await material_service.create(material_data)

        return material
    
    except (CompanyNotFound, SupplierNotFound) as e:

        raise map_exception(e)

