from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import (
    CompanyNotFound,
    SupplierNotFound,
    SupplierAccesDenied
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import (
    LegalEntityRepository,
    SupplierRepository,
    CompanyRepository
)
from api.core.database import get_session
from api.schemas import (
    SupplierSchema,
    SupplierPublicSchema,
    SupplierUpdateSchema,
    ListSupplierPublicSchema
)
from api.services.suppliers import SupplierService
from api.security.dependencies import CurrentUser

supplier_router = APIRouter(
    prefix = "/api/suppliers",
    tags = ["Suppliers"]
)

def get_legal_entity_repository(db: AsyncSession = Depends(get_session)) -> LegalEntityRepository:

    return LegalEntityRepository(db)

def get_supplier_repository(db: AsyncSession = Depends(get_session)) -> SupplierRepository:

    return SupplierRepository(db)

def get_company_repository(db: AsyncSession = Depends(get_session)) -> CompanyRepository:

    return CompanyRepository(db)

def get_supplier_service(
    legal_entity_repository: LegalEntityRepository = Depends(get_legal_entity_repository),
    supplier_repository: SupplierRepository = Depends(get_supplier_repository),
    company_repository: CompanyRepository = Depends(get_company_repository),
) -> SupplierService:

    return SupplierService(
        legal_entity_repository=legal_entity_repository,
        supplier_repository=supplier_repository,
        company_repository=company_repository
    )


@supplier_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Criando um fornecedor",
    response_model=SupplierPublicSchema
)
async def create_supplier(
    supplier_data: SupplierSchema,
    db: AsyncSession = Depends(get_session),
    supplier_service: SupplierService = Depends(get_supplier_service),
    current_user: CurrentUser = CurrentUser,
):
    async with db.begin():

        return await supplier_service.create(supplier_data)


@supplier_router.get(
    path = "/{company_id}",
    status_code = status.HTTP_200_OK,
    summary = "Listando os fornecedores",
    response_model = ListSupplierPublicSchema
)
async def list_suppliers(
    company_id: int,
    supplier_service: SupplierService = Depends(get_supplier_service),
    current_user: CurrentUser = CurrentUser,
    offset: int = Query(0, ge = 0, description = "Registros a serem pulados"),
    limit: int = Query(20, ge = 1, description = "Qtd máxima de registros apresentados"),
    search: Optional[str] = Query(None, description = "Pesquisar pelo nome de algum fornecedor")
):
    suppliers = await supplier_service.list(
        company_id, offset, limit, search
    )

    return {
        "suppliers": suppliers
    }


@supplier_router.get(
    path = "/{company_id}/{supplier_id}",
    status_code = status.HTTP_200_OK,
    summary = "Selecionando um fornecedor específico",
    response_model = SupplierPublicSchema
)
async def get_supplier(
    company_id: int,
    supplier_id: int,
    service: SupplierService = Depends(get_supplier_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        supplier = await service.get(company_id, supplier_id)
        return supplier

    except (CompanyNotFound, SupplierNotFound) as e:
        raise map_exception(e)


@supplier_router.delete(
    path = "/{company_id}/{supplier_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Deletando um fornecedor específico"
)
async def delete_supplier(
    company_id: int,
    supplier_id: int,
    service: SupplierService = Depends(get_supplier_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        await service.delete(company_id, supplier_id)

    except (CompanyNotFound, SupplierNotFound) as e:
        raise map_exception(e)


@supplier_router.put(
    path = "/{supplier_id}",
    status_code = status.HTTP_200_OK,
    summary = "Atualizando um fornecedor",
    response_model = SupplierPublicSchema
)
async def update_supplier(
    supplier_id: int,
    supplier_data: SupplierUpdateSchema,
    service: SupplierService = Depends(get_supplier_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        supplier_info = supplier_data.model_dump(exclude_unset = True)
        supplier = await service.update(supplier_id, supplier_info)
        return supplier

    except (CompanyNotFound, SupplierNotFound, SupplierAccesDenied) as e:
        raise map_exception(e)
