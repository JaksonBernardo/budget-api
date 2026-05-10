import logging

from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import LoginSchema, LoginResponseSchema
from api.repositories.users import UserRepository
from api.core.database import get_session
from api.security.password import verify_password
from api.security.jwt import create_access_token
from api.exceptions.users import UserNotFound
from api.exceptions.map_exceptions import map_exception

auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)



def get_user_repository(db: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(db)


@auth_router.post(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Rota de autenticação para acesso à API",
    response_model=LoginResponseSchema
)
async def auth(
    login_data: LoginSchema,
    response: Response,
    user_repo: UserRepository = Depends(get_user_repository)
):
    try:
        user = await user_repo.get_by_email(login_data.email)
        if not user or not verify_password(user.password, login_data.password):
            raise UserNotFound("Credenciais inválidas")

        access_token = create_access_token(subject=user.id, company_id=user.company_id, username=user.name)
        
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,  # Set to True in production (HTTPS)
            samesite="lax",
            max_age=3600 # 1 hour
        )
        
        return LoginResponseSchema(
            name=user.name,
            email=user.email,
            company_id=user.company_id
        )

    except UserNotFound as e:
        raise map_exception(e)


@auth_router.post(
    path="/logout",
    status_code=status.HTTP_200_OK,
    summary="Rota para logout, removendo o cookie de acesso",
)
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )
    return {"message": "Logout realizado com sucesso"}
