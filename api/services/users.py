from typing import List, Optional
from api.models import User
from api.repositories.users import UserRepository
from api.repositories.companys import CompanyRepository
from api.schemas.users import UserCreateSchema, UserUpdateSchema
from api.security.password import hash_password, verify_password
from api.exceptions.users import (
    UserNotFound,
    UserAlreadyExists,
    UserAccessDenied
)
from api.exceptions.companys import CompanyNotFound


class UserService:

    def __init__(
        self,
        user_repository: UserRepository,
        company_repository: CompanyRepository
    ):
        self.__user_repository = user_repository
        self.__company_repository = company_repository

    async def create(self, user_data: UserCreateSchema) -> User:
        """Cria um novo usuário com hash de senha."""
        # Verifica se empresa existe
        company = await self.__company_repository.get_by_id(user_data.company_id)
        if not company:
            raise CompanyNotFound()

        # Verifica se e-mail já existe
        existing_user = await self.__user_repository.get_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExists()

        user = User(
            name=user_data.name,
            email=user_data.email,
            password=hash_password(user_data.password),
            whatsapp=user_data.whatsapp,
            photo=user_data.photo,
            profile=user_data.profile,
            company_id=user_data.company_id
        )

        return await self.__user_repository.save(user)

    async def get_by_id_and_company(self, company_id: int, user_id: int) -> User:
        """Busca um usuário por ID e empresa."""
        user = await self.__user_repository.get_by_id_and_company(company_id, user_id)
        if not user:
            raise UserNotFound()
        return user

    async def list_by_company(
        self,
        company_id: int,
        offset: int = 0,
        limit: int = 20,
        search: Optional[str] = None
    ) -> List[User]:
        """Lista usuários de uma empresa."""
        # Verifica se empresa existe
        company = await self.__company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFound()

        return await self.__user_repository.get_by_company_id(
            company_id, offset, limit, search
        )

    async def update(self, user_id: int, user_data: UserUpdateSchema) -> User:
        """Atualiza os dados de um usuário."""
        user = await self.__user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound()

        update_data = user_data.model_dump(exclude_unset=True)

        # Se tem e-mail, verifica se não está sendo usado por outro usuário
        if "email" in update_data and update_data["email"] != user.email:
            existing_user = await self.__user_repository.get_by_email(update_data["email"])
            if existing_user:
                raise UserAlreadyExists()

        # Se tem senha, faz o hash
        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])

        # Aplica as atualizações
        for key, value in update_data.items():
            setattr(user, key, value)

        return await self.__user_repository.update(user)

    async def delete(self, user_id: int) -> None:
        """Deleta um usuário."""
        deleted = await self.__user_repository.delete_by_id(user_id)
        if not deleted:
            raise UserNotFound()

    async def authenticate(self, email: str, password: str) -> User:
        """Autentica um usuário com e-mail e senha."""
        user = await self.__user_repository.get_by_email(email)
        if not user:
            raise UserNotFound("Credenciais inválidas")

        if not verify_password(user.password, password):
            raise UserNotFound("Credenciais inválidas")

        return user
