from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import Supplier, LegalEntity
from api.repositories import (
    SupplierRepository,
    CompanyRepository,
    LegalEntityRepository
)
from api.schemas import SupplierSchema, SupplierPublicSchema, SupplierUpdateSchema
from api.exceptions import (
    CompanyNotFound,
    SupplierNotFound,
    SupplierAccesDenied
)


class SupplierService:

    def __init__(
        self,
        db: AsyncSession,
        legal_entity_repository: LegalEntityRepository,
        supplier_repository: SupplierRepository,
        company_repository: CompanyRepository
    ):  
        self.__db = db
        self._legal_entity_repository = legal_entity_repository
        self._supplier_repository = supplier_repository
        self._company_repository = company_repository

    async def create(self, supplier_data: SupplierSchema) -> SupplierPublicSchema:

        company = await self._company_repository.get_by_id(supplier_data.company_id)

        if not company:
            raise CompanyNotFound()

        new_legal_entity_db = LegalEntity(
            companie=supplier_data.companie,
            cpf_cnpj=supplier_data.cpf_cnpj,
            email=supplier_data.email,
            phone=supplier_data.phone,
            address=supplier_data.address,
            number=supplier_data.number,
            state=supplier_data.state,
            cep=supplier_data.cep,
            city=supplier_data.city
        )

        await self._legal_entity_repository.save(new_legal_entity_db)

        new_supplier_db = Supplier(
            id_person=new_legal_entity_db.id,
            company_id=supplier_data.company_id
        )

        await self._supplier_repository.save(new_supplier_db)

        new_supplier = await self._supplier_repository.get_by_id(new_supplier_db.id)

        return new_supplier

    async def list(
        self,
        company_id: int,
        offset: int = 0,
        limit: int = 20,
        search: Optional[str] = None
    ) -> List[SupplierPublicSchema]:

        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFound()

        suppliers = await self._supplier_repository.get_by_company_id(
            company_id, offset, limit, search
        )

        return suppliers

    async def get(self, company_id: int, supplier_id: int) -> SupplierPublicSchema:
        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFound()

        supplier = await self._supplier_repository.get_by_id_and_company(company_id, supplier_id)

        if not supplier:
            raise SupplierNotFound()

        return supplier

    async def delete(self, company_id: int, supplier_id: int) -> None:

        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFound()

        supplier = await self._supplier_repository.get_by_id_and_company(company_id, supplier_id)

        if not supplier:
            raise SupplierNotFound()

        await self._supplier_repository.delete_by_id(company_id, supplier_id)

    async def update(self, supplier_id: int, supplier_data: Dict) -> SupplierPublicSchema:
            
        company = await self._company_repository.get_by_id(supplier_data["company_id"])

        if not company:
            raise CompanyNotFound()

        supplier = await self._supplier_repository.get_by_id_and_company(
            supplier_data["company_id"],
            supplier_id
        )

        if not supplier:
            raise SupplierNotFound()

        if "company_id" in supplier_data and supplier.company_id != supplier_data["company_id"]:
            raise SupplierAccesDenied()

        legal_entity = supplier.legal_entity

        if "companie" in supplier_data:
            legal_entity.companie = supplier_data["companie"]
        if "cpf_cnpj" in supplier_data:
            legal_entity.cpf_cnpj = supplier_data["cpf_cnpj"]
        if "email" in supplier_data:
            legal_entity.email = supplier_data["email"]
        if "phone" in supplier_data:
            legal_entity.phone = supplier_data["phone"]
        if "address" in supplier_data:
            legal_entity.address = supplier_data["address"]
        if "number" in supplier_data:
            legal_entity.number = supplier_data["number"]
        if "state" in supplier_data:
            legal_entity.state = supplier_data["state"]
        if "cep" in supplier_data:
            legal_entity.cep = supplier_data["cep"]
        if "city" in supplier_data:
            legal_entity.city = supplier_data["city"]

        supplier.updated_at = datetime.now()

        await self._legal_entity_repository.update(legal_entity)

        updated_supplier = await self._supplier_repository.get_by_id_and_company(
            supplier_data["company_id"],
            supplier_id
        )

        return updated_supplier
