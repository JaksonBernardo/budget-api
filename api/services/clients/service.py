from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import Client, LegalEntity
from api.repositories import (
    ClientRepository,
    CompanyRepository,
    LegalEntityRepository
)
from api.schemas import ClientSchema, ClientPublicSchema, ClientUpdateSchema
from api.exceptions import (
    CompanyNotFound,
    ClientNotFound,
    ClientAccesDenied
)


class ClientService:

    def __init__(
        self,
        legal_entity_repository: LegalEntityRepository,
        client_repository: ClientRepository,
        company_repository: CompanyRepository
    ):
        self._legal_entity_repository = legal_entity_repository
        self._client_repository = client_repository
        self._company_repository = company_repository

    async def create(self, client_data: ClientSchema) -> ClientPublicSchema:

        company = await self._company_repository.get_by_id(client_data.company_id)

        if not company:
            raise CompanyNotFound()

        new_legal_entity_db = LegalEntity(
            companie=client_data.companie,
            cpf_cnpj=client_data.cpf_cnpj,
            email=client_data.email,
            phone=client_data.phone,
            address=client_data.address,
            number=client_data.number,
            state=client_data.state,
            cep=client_data.cep,
            city=client_data.city
        )

        await self._legal_entity_repository.save(new_legal_entity_db)

        new_client_db = Client(
            id_person=new_legal_entity_db.id,
            company_id=client_data.company_id
        )

        await self._client_repository.save(new_client_db)

        new_client = await self._client_repository.get_by_id(new_client_db.id)

        return new_client

    async def list(
        self,
        company_id: int,
        offset: int = 0,
        limit: int = 20,
        search: Optional[str] = None
    ) -> List[ClientPublicSchema]:

        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFound()

        clients = await self._client_repository.get_by_company_id(
            company_id, offset, limit, search
        )

        return clients

    async def get(self, company_id: int, client_id: int) -> ClientPublicSchema:
        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFound()

        client = await self._client_repository.get_by_id_and_company(company_id, client_id)

        if not client:
            raise ClientNotFound()

        return client

    async def delete(self, company_id: int, client_id: int) -> None:
        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFound()

        client = await self._client_repository.get_by_id_and_company(company_id, client_id)

        if not client:
            raise ClientNotFound()

        await self._client_repository.delete_by_id(company_id, client_id)

    async def update(self, client_id: int, client_data: Dict) -> ClientPublicSchema:
        company = await self._company_repository.get_by_id(client_data["company_id"])

        if not company:
            raise CompanyNotFound()

        client = await self._client_repository.get_by_id_and_company(
            client_data["company_id"],
            client_id
        )

        if not client:
            raise ClientNotFound()

        if "company_id" in client_data and client.company_id != client_data["company_id"]:
            raise ClientAccesDenied()

        legal_entity = client.legal_entity

        if "companie" in client_data:
            legal_entity.companie = client_data["companie"]
        if "cpf_cnpj" in client_data:
            legal_entity.cpf_cnpj = client_data["cpf_cnpj"]
        if "email" in client_data:
            legal_entity.email = client_data["email"]
        if "phone" in client_data:
            legal_entity.phone = client_data["phone"]
        if "address" in client_data:
            legal_entity.address = client_data["address"]
        if "number" in client_data:
            legal_entity.number = client_data["number"]
        if "state" in client_data:
            legal_entity.state = client_data["state"]
        if "cep" in client_data:
            legal_entity.cep = client_data["cep"]
        if "city" in client_data:
            legal_entity.city = client_data["city"]

        await self._legal_entity_repository.update(legal_entity)

        updated_client = await self._client_repository.get_by_id_and_company(
            client_data["company_id"],
            client_id
        )

        return updated_client

        