from typing import Dict, List, Optional
from api.models import Material
from api.repositories import (
    MaterialRepository,
    SupplierRepository,
    CompanyRepository,
)
from api.schemas import (
    MaterialSchema,
    MaterialPublicSchema,
)
from api.exceptions import (
    CompanyNotFound,
    MaterialNotFound,
    SupplierNotFound
)


class MaterialService:

    def __init__(
        self,
        material_repository: MaterialRepository,
        supplier_repository: SupplierRepository,
        company_repository: CompanyRepository
    ):
        
        self._material_repository = material_repository
        self._supplier_repository = supplier_repository
        self._company_repository = company_repository

    async def create(self, material_data: MaterialSchema) -> Material:

        company = await self._company_repository.get_by_id(
            material_data.company_id
        )

        if not company:

            raise CompanyNotFound()
        
        supplier = await self._supplier_repository.get_by_id(
            material_data.supplier_id
        )

        if not supplier:

            raise SupplierNotFound()
        
        material_db = Material(
            name = material_data.name,
            unit_cost = material_data.unit_cost,
            classification = material_data.classification,
            supplier_id = material_data.supplier_id,
            company_id = material_data.company_id
        )

        new_material = await self._material_repository.save(
            material_db
        )

        return new_material


    async def list(
        self,
        company_id: int,
        offset: int = 0,
        limit: int = 20,
        name: Optional[str] = None,
        supplier: Optional[str] = None
    ) -> List[MaterialPublicSchema]:

        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFound()

        materials = await self._material_repository.get_by_company_id(
            company_id,
            offset,
            limit,
            name,
            supplier
        )

        return materials
    


