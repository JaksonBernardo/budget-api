from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_session
from api.repositories.users import UserRepository
from api.security.jwt import decode_access_token
from api.models import User

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: AsyncSession = Depends(get_session)
) -> User:

    user_id = decode_access_token(credentials.credentials)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_repo = UserRepository(db)

    user = await user_repo.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
