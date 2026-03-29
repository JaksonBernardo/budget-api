from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, field_validator
from datetime import datetime

from api.models import Classificate
from api.exceptions.companys import (
    InvalidTypeCompanyId, 
    ZeroCompanyId
)
from api.exceptions.suppliers import (
    SupplierNotFound,
    ZeroSupplierId
)
from api.exceptions.materials import (
    MaterialInvalidName, 
    MaterialInvalidClassification
)


class MaterialSchema(BaseModel):

    name: str
    unit_cost: Decimal
    classification: Classificate
    supplier_id: int
    company_id: int

    @field_validator("name")
    def validate_name(cls, value):

        if not isinstance(value, str):

            raise TypeError("Name tem que ser do tipo string")

        if not value:

            raise MaterialInvalidName()
        
        return value
    
    @field_validator("unit_cost")
    def validate_unit_cost(cls, value):

        if value < 0:

            raise ValueError("Custo unitário não pode ser negativo")
        
        return value
    
    @field_validator("classification")
    def validate_classification(cls, value):

        if not isinstance(value, str):

            raise TypeError("Classification tem que ser do tipo string")
        
        if value != Classificate.DIRECT and value != Classificate.INDIRECT:

            raise MaterialInvalidClassification()
        
        return value
    
    @field_validator("company_id")
    def validate_company_id(cls, value):

        if not isinstance(value, int):

            raise InvalidTypeCompanyId()
        
        if value <= 0:

            raise ZeroCompanyId()
        
        return value
    
    @field_validator("supplier_id")
    def validate_supplier_id(cls, value):

        if not isinstance(value, int):

            raise TypeError("ID Supplier tem que do tipo inteiro")
        
        if value <= 0:

            raise ZeroSupplierId()
        
        return value


class MaterialPublicSchema(BaseModel):

    id: int
    unit_cost: Decimal
    stock: int
    classification: Classificate
    supplier_id: int
    company_id: int


class MaterialUpdateSchema(BaseModel):

    name: Optional[str]
    unit_cost: Optional[Decimal]
    classification: Optional[Classificate]
    supplier_id: Optional[int]
    company_id: Optional[int]

    @field_validator("name")
    def validate_name(cls, value):

        if not isinstance(value, str):

            raise TypeError("Name tem que ser do tipo string")

        if not value:

            raise MaterialInvalidName()
        
        return value
    
    @field_validator("unit_cost")
    def validate_unit_cost(cls, value):

        if value < 0:

            raise ValueError("Custo unitário não pode ser negativo")
        
        return value
    
    @field_validator("classification")
    def validate_classification(cls, value):

        if not isinstance(value, str):

            raise TypeError("Classification tem que ser do tipo string")
        
        if value != Classificate.DIRECT and value != Classificate.INDIRECT:

            raise MaterialInvalidClassification()
        
        return value
    
    @field_validator("company_id")
    def validate_company_id(cls, value):

        if not isinstance(value, int):

            raise InvalidTypeCompanyId()
        
        if value <= 0:

            raise ZeroCompanyId()
        
        return value
    
    @field_validator("supplier_id")
    def validate_supplier_id(cls, value):

        if not isinstance(value, int):

            raise TypeError("ID Supplier tem que do tipo inteiro")
        
        if value <= 0:

            raise ZeroSupplierId()
        
        return value


class ListMaterialPublicSchema(BaseModel):

    materials: List[MaterialPublicSchema]


