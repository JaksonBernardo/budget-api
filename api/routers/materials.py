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
from api.services.materials import MaterialService
from api.security.dependencies import CurrentUser


material_router = APIRouter(
    prefix = "/api/v1/materials",
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
    supplier_repository: SupplierRepository = Depends(get_supplier_repository),
    company_repository: CompanyRepository = Depends(get_company_repository),
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
    service: MaterialService = Depends(get_material_service),
    current_user: CurrentUser = CurrentUser,
):

    try:

        material = await service.create(material_data)

        return material

    except (CompanyNotFound, SupplierNotFound) as e:

        raise map_exception(e)


@material_router.get(
    path = "/{company_id}",
    status_code = status.HTTP_200_OK,
    summary = "Listando os materiais pelo company_id",
    response_model = ListMaterialPublicSchema
)
async def list_materials(
    company_id: int,
    service: MaterialService = Depends(get_material_service),
    current_user: CurrentUser = CurrentUser,
    offset: int = Query(0, ge = 0, description = "Registros a serem pulados"),
    limit: int = Query(20, ge = 1, le = 100, description = "Qtd máxima de registros apresentados"),
    name: Optional[str] = Query(None, description = "Pesquisar pelo nome de algum material"),
    supplier: Optional[str] = Query(None, description = "Pesquisar pelo nome de algum fornecedor"),
):

    try:

        materials = await service.list(
            company_id,
            offset,
            limit,
            name,
            supplier
        )

        return {
            "materials": materials,
            "limit": limit,
            "offset": offset
        }

    except (CompanyNotFound, ) as e:

        raise map_exception(e)


@material_router.get(
    path = "/{company_id}/{material_id}",
    status_code = status.HTTP_200_OK,
    summary = "Selecionando um material específico",
    response_model = MaterialPublicSchema
)
async def get_material(
    company_id: int,
    material_id: int,
    service: MaterialService = Depends(get_material_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        material = await service.get(company_id, material_id)
        return material

    except (CompanyNotFound, MaterialNotFound) as e:
        raise map_exception(e)


@material_router.delete(
    path = "/{company_id}/{material_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Deletando um material específico"
)
async def delete_material(
    company_id: int,
    material_id: int,
    service: MaterialService = Depends(get_material_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        await service.delete(company_id, material_id)

    except (CompanyNotFound, MaterialNotFound) as e:
        raise map_exception(e)


@material_router.put(
    path = "/{material_id}",
    status_code = status.HTTP_200_OK,
    summary = "Atualizando um material",
    response_model = MaterialPublicSchema
)
async def update_material(
    material_id: int,
    material_data: MaterialUpdateSchema,
    service: MaterialService = Depends(get_material_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        material_info = material_data.model_dump(exclude_unset = True)
        material = await service.update(material_id, material_info)
        return material

    except (CompanyNotFound, MaterialNotFound, SupplierNotFound, MaterialInvalidName) as e:
        raise map_exception(e)


