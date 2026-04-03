from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from api.models import User


class UserRepository:

    def __init__(self, db: AsyncSession):
        self.__db = db

    async def save(self, user: User) -> User:
        """Persiste um novo usuário no banco."""
        self.__db.add(user)
        await self.__db.commit()
        await self.__db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        """Busca um usuário pelo ID."""
        query = select(User).where(User.id == user_id)
        result = await self.__db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id_and_company(self, company_id: int, user_id: int) -> User | None:
        """Busca um usuário pelo ID e empresa."""
        query = select(User).where(
            User.id == user_id,
            User.company_id == company_id
        )
        result = await self.__db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Busca um usuário pelo e-mail."""
        query = select(User).where(User.email == email)
        result = await self.__db.execute(query)
        return result.scalar_one_or_none()

    async def update(self, user: User) -> User:
        """Atualiza os dados de um usuário."""
        try:
            await self.__db.merge(user)
            await self.__db.commit()
            await self.__db.refresh(user)
            return user
        except Exception:
            await self.__db.rollback()
            raise

    async def delete_by_id(self, user_id: int) -> bool:
        """Deleta um usuário pelo ID. Retorna False se não encontrou."""
        try:
            user = await self.get_by_id(user_id)
            if not user:
                return False

            await self.__db.execute(delete(User).where(User.id == user_id))
            await self.__db.commit()
            return True
        except Exception:
            await self.__db.rollback()
            raise

    async def get_by_company_id(
        self,
        company_id: int,
        offset: int = 0,
        limit: int = 20,
        search: Optional[str] = None
    ) -> List[User]:
        """Lista usuários de uma empresa com paginação e busca opcional."""
        query = select(User).where(User.company_id == company_id)

        if search:
            query = query.where(User.name.ilike(f"%{search}%"))

        query = query.offset(offset).limit(limit)
        result = await self.__db.execute(query)
        return result.scalars().all()
