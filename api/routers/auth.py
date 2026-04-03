from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import LoginSchema, Token

auth_router = APIRouter(
    prefix = "/api/auth",
    tags = ["Auth"]
)


@auth_router.post(
    path = "/",
    status_code = status.HTTP_200_OK,
    summary = "Rota de autenticacao para acesso a api",
    response_model = Token
)
async def auth(
    login_data: LoginSchema
):
    
    pass

