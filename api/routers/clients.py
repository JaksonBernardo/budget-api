from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import (
    CompanyNotFound,
    ClientNotFound
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import ClientRepository, CompanyRepository
from api.core.database import get_session
from api.schemas import (
    ClientSchema,
    ClientPublicSchema,
    ClientUpdateSchema,
    ListClientPublicSchema
)

client_router = APIRouter(
    prefix = "/api/clients",
    tags = ["Clients"]
)


def get_client_repository(db: AsyncSession = Depends(get_session)) -> ClientRepository:

    return ClientRepository(db)

def get_company_repository(db: AsyncSession = Depends(get_session)) -> CompanyRepository:

    return CompanyRepository(db)


@client_router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Criando um cliente",
    response_model=0
)
async def create_client(
    client_data: ClientSchema,
    client_repository: ClientRepository = Depends(get_client_repository),
    company_repository: CompanyRepository = Depends(get_company_repository),
):
    
    pass

