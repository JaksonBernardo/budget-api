from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import (
    CompanyNotFound,
    ClientNotFound,
    ClientAccesDenied
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import (
    LegalEntityRepository,
    ClientRepository,
    CompanyRepository
)
from api.core.database import get_session
from api.schemas import (
    ClientSchema,
    ClientPublicSchema,
    ClientUpdateSchema,
    ListClientPublicSchema
)
from api.services.clients import ClientService
from api.security.dependencies import CurrentUser

client_router = APIRouter(
    prefix = "/api/clients",
    tags = ["Clients"]
)

def get_legal_entity_repository(db: AsyncSession = Depends(get_session)) -> LegalEntityRepository:

    return LegalEntityRepository(db)

def get_client_repository(db: AsyncSession = Depends(get_session)) -> ClientRepository:

    return ClientRepository(db)

def get_company_repository(db: AsyncSession = Depends(get_session)) -> CompanyRepository:

    return CompanyRepository(db)

def get_client_service(
    legal_entity_repository: LegalEntityRepository = Depends(get_legal_entity_repository),
    client_repository: ClientRepository = Depends(get_client_repository),
    company_repository: CompanyRepository = Depends(get_company_repository),
) -> ClientService:

    return ClientService(
        legal_entity_repository=legal_entity_repository,
        client_repository=client_repository,
        company_repository=company_repository
    )


@client_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Criando um cliente",
    response_model=ClientPublicSchema
)
async def create_client(
    client_data: ClientSchema,
    db: AsyncSession = Depends(get_session),
    client_service: ClientService = Depends(get_client_service),
    current_user: CurrentUser = CurrentUser,
):
    async with db.begin():

        return await client_service.create(client_data)


@client_router.get(
    path = "/{company_id}",
    status_code = status.HTTP_200_OK,
    summary = "Listando os clientes",
    response_model = ListClientPublicSchema
)
async def list_clients(
    company_id: int,
    client_service: ClientService = Depends(get_client_service),
    current_user: CurrentUser = CurrentUser,
    offset: int = Query(0, ge = 0, description = "Registros a serem pulados"),
    limit: int = Query(20, ge = 1, description = "Qtd máxima de registros apresentados"),
    search: Optional[str] = Query(None, description = "Pesquisar pelo nome de algum cliente")
):
    clients = await client_service.list(
        company_id, offset, limit, search
    )

    return {
        "clients": clients
    }


@client_router.get(
    path = "/{company_id}/{client_id}",
    status_code = status.HTTP_200_OK,
    summary = "Selecionando um cliente específico",
    response_model = ClientPublicSchema
)
async def get_client(
    company_id: int,
    client_id: int,
    service: ClientService = Depends(get_client_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        client = await service.get(company_id, client_id)
        return client

    except (CompanyNotFound, ClientNotFound) as e:
        raise map_exception(e)


@client_router.delete(
    path = "/{company_id}/{client_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Deletando um cliente específico"
)
async def delete_client(
    company_id: int,
    client_id: int,
    service: ClientService = Depends(get_client_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        await service.delete(company_id, client_id)

    except (CompanyNotFound, ClientNotFound) as e:
        raise map_exception(e)


@client_router.put(
    path = "/{client_id}",
    status_code = status.HTTP_200_OK,
    summary = "Atualizando um cliente",
    response_model = ClientPublicSchema
)
async def update_client(
    client_id: int,
    client_data: ClientUpdateSchema,
    service: ClientService = Depends(get_client_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        client_info = client_data.model_dump(exclude_unset = True)
        client = await service.update(client_id, client_info)
        return client

    except (CompanyNotFound, ClientNotFound, ClientAccesDenied) as e:
        raise map_exception(e)


