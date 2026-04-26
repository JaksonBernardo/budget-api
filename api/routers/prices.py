from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import (
    CompanyNotFound,
)
from api.exceptions.prices import (
    PriceNotFound,
    PriceInvalidName,
    PriceInvalidValue,
    PriceExceedValue
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import (
    PriceRepository,
    CompanyRepository
)
from api.core.database import get_session
from api.schemas import (
    PriceSchema,
    PricePublicSchema,
    PriceUpdateSchema,
    ListPricePublicSchema
)
from api.services.prices import PriceService
from api.security.dependencies import CurrentUser


price_router = APIRouter(
    prefix = "/api/v1/prices",
    tags = ["Prices"]
)


def get_price_repository(
    db: AsyncSession = Depends(get_session)
) -> PriceRepository:
    return PriceRepository(db)

def get_company_repository(
    db: AsyncSession = Depends(get_session)
) -> CompanyRepository:
    return CompanyRepository(db)

def get_price_service(
    price_repository: PriceRepository = Depends(get_price_repository),
    company_repository: CompanyRepository = Depends(get_company_repository),
) -> PriceService:
    return PriceService(
        price_repository,
        company_repository
    )


@price_router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Criando um preço",
    response_model = PricePublicSchema
)
async def create_price(
    price_data: PriceSchema,
    service: PriceService = Depends(get_price_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        price = await service.create(price_data)
        return price
    except (CompanyNotFound, PriceInvalidName, PriceInvalidValue, PriceExceedValue) as e:
        raise map_exception(e)


@price_router.get(
    path = "/{company_id}",
    status_code = status.HTTP_200_OK,
    summary = "Listando os preços pelo company_id",
    response_model = ListPricePublicSchema
)
async def list_prices(
    company_id: int,
    service: PriceService = Depends(get_price_service),
    current_user: CurrentUser = CurrentUser,
    offset: int = Query(0, ge = 0, description = "Registros a serem pulados"),
    limit: int = Query(20, ge = 1, le = 100, description = "Qtd máxima de registros apresentados"),
    name: Optional[str] = Query(None, description = "Pesquisar pelo nome de algum preço"),
):
    try:
        prices = await service.list(
            company_id,
            offset,
            limit,
            name
        )
        return {
            "prices": prices,
            "limit": limit,
            "offset": offset
        }
    except (CompanyNotFound, ) as e:
        raise map_exception(e)


@price_router.get(
    path = "/{company_id}/{price_id}",
    status_code = status.HTTP_200_OK,
    summary = "Selecionando um preço específico",
    response_model = PricePublicSchema
)
async def get_price(
    company_id: int,
    price_id: int,
    service: PriceService = Depends(get_price_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        price = await service.get(company_id, price_id)
        return price
    except (CompanyNotFound, PriceNotFound) as e:
        raise map_exception(e)


@price_router.delete(
    path = "/{company_id}/{price_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Deletando um preço específico"
)
async def delete_price(
    company_id: int,
    price_id: int,
    service: PriceService = Depends(get_price_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        await service.delete(company_id, price_id)
    except (CompanyNotFound, PriceNotFound) as e:
        raise map_exception(e)


@price_router.put(
    path = "/{company_id}/{price_id}",
    status_code = status.HTTP_200_OK,
    summary = "Atualizando um preço",
    response_model = PricePublicSchema
)
async def update_price(
    company_id: int,
    price_id: int,
    price_data: PriceUpdateSchema,
    service: PriceService = Depends(get_price_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        price_info = price_data.model_dump(exclude_unset = True)
        price = await service.update(company_id, price_id, price_info)
        return price
    except (CompanyNotFound, PriceNotFound, PriceInvalidName, PriceInvalidValue, PriceExceedValue) as e:
        raise map_exception(e)
