from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import Client, LegalEntity
from api.repositories import (
    ClientRepository,
    CompanyRepository,
    LegalEntityRepository
)
from api.schemas import ClientSchema, ClientPublicSchema
from api.exceptions import (
    CompanyNotFound,
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

        