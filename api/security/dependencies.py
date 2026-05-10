from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_session
from api.repositories.users import UserRepository
from api.security.jwt import decode_access_token
from api.models import User

cookie_scheme = APIKeyCookie(name="access_token", auto_error=False)


async def get_current_user(
    token: Annotated[Optional[str], Depends(cookie_scheme)],
    db: AsyncSession = Depends(get_session)
) -> User:

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não encontrado nos cookies",
        )

    user_id = decode_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )

    user_repo = UserRepository(db)

    user = await user_repo.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
