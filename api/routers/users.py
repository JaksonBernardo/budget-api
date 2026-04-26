from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions.users import UserNotFound, UserAlreadyExists
from api.exceptions.companys import CompanyNotFound
from api.exceptions.map_exceptions import map_exception
from api.repositories import UserRepository, CompanyRepository
from api.core.database import get_session
from api.schemas.users import (
    UserCreateSchema,
    UserUpdateSchema,
    UserPublicSchema,
    ListUserPublicSchema
)
from api.services.users import UserService
from api.security.dependencies import CurrentUser

user_router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)


def get_user_repository(db: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(db)


def get_company_repository(db: AsyncSession = Depends(get_session)) -> CompanyRepository:
    return CompanyRepository(db)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    company_repository: CompanyRepository = Depends(get_company_repository)
) -> UserService:
    return UserService(
        user_repository=user_repository,
        company_repository=company_repository
    )


@user_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Criando um usuário",
    response_model=UserPublicSchema
)
async def create_user(
    user_data: UserCreateSchema,
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = await user_service.create(user_data)
        return user

    except (CompanyNotFound, UserAlreadyExists) as e:
        raise map_exception(e)


@user_router.get(
    path="/{company_id}",
    status_code=status.HTTP_200_OK,
    summary="Listando usuários de uma empresa",
    response_model=ListUserPublicSchema
)
async def list_users(
    company_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = CurrentUser,
    offset: int = Query(0, ge=0, description="Registros a serem pulados"),
    limit: int = Query(20, ge=1, description="Qtd máxima de registros apresentados"),
    search: Optional[str] = Query(None, description="Pesquisar pelo nome do usuário")
):
    try:
        users = await user_service.list_by_company(company_id, offset, limit, search)
        return {
            "users": users,
            "limit": limit,
            "offset": offset
        }

    except CompanyNotFound as e:
        raise map_exception(e)


@user_router.get(
    path="/{company_id}/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Selecionando um usuário específico",
    response_model=UserPublicSchema
)
async def get_user(
    company_id: int,
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        user = await user_service.get_by_id_and_company(company_id, user_id)
        return user

    except UserNotFound as e:
        raise map_exception(e)


@user_router.put(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualizando um usuário",
    response_model=UserPublicSchema
)
async def update_user(
    user_id: int,
    user_data: UserUpdateSchema,
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        user = await user_service.update(user_id, user_data)
        return user

    except (UserNotFound, UserAlreadyExists) as e:
        raise map_exception(e)


@user_router.delete(
    path="/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletando um usuário"
)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        await user_service.delete(user_id)

    except UserNotFound as e:
        raise map_exception(e)
