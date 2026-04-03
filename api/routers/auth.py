from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import LoginSchema, Token
from api.repositories.users import UserRepository
from api.core.database import get_session
from api.security.password import verify_password
from api.security.jwt import create_access_token
from api.exceptions.users import UserNotFound
from api.exceptions.map_exceptions import map_exception

auth_router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)


def get_user_repository(db: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(db)


@auth_router.post(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Rota de autenticação para acesso à API",
    response_model=Token
)
async def auth(
    login_data: LoginSchema,
    user_repo: UserRepository = Depends(get_user_repository)
):
    try:
        user = await user_repo.get_by_email(login_data.email)
        if not user or not verify_password(user.password, login_data.password):
            raise UserNotFound("Credenciais inválidas")

        access_token = create_access_token(subject=user.id)
        return Token(access_token=access_token, token_type="bearer")

    except UserNotFound as e:
        raise map_exception(e)
