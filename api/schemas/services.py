from typing import List, Optional
from pydantic import BaseModel, Field
from decimal import Decimal

 
class ServiceMaterialSchema(BaseModel):
    material_id: int
    qtd_material: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class ServicePublicMaterialSchema(BaseModel):
    material_id: int
    qtd_material: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    total_cost: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class ServiceEmployeeSchema(BaseModel):
    employee_id: int
    minute_works: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class ServicePublicEmployeeSchema(BaseModel):
    employee_id: int
    minute_works: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    total_cost: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class ServicePriceSchema(BaseModel):
    price_id: int
    fixed_expenses: Decimal = Field(ge=0, le=100)
    impost: Decimal = Field(ge=0, le=100)
    commission: Decimal = Field(ge=0, le=100)
    others_rates: Decimal = Field(ge=0, le=100)
    profit_margin: Decimal = Field(ge=0, le=100)


class ServicePublicPriceSchema(BaseModel):
    price_id: int
    fixed_expenses: Decimal = Field(ge=0, le=100)
    impost: Decimal = Field(ge=0, le=100)
    commission: Decimal = Field(ge=0, le=100)
    others_rates: Decimal = Field(ge=0, le=100)
    profit_margin: Decimal = Field(ge=0, le=100)
    value: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class ServiceSchema(BaseModel):

    name: str
    segment_id: int
    description: Optional[str] = None
    company_id: int

    materials: List[ServiceMaterialSchema] = []
    employees: List[ServiceEmployeeSchema] = []
    prices: List[ServicePriceSchema] = []


class ServicePublicSchema(BaseModel):

    id: int
    name: str
    segment_id: int
    description: Optional[str] = None
    company_id: int

    materials: List[ServicePublicMaterialSchema] = []
    employees: List[ServicePublicEmployeeSchema] = []
    prices: List[ServicePublicPriceSchema] = []








class ListServicePublicSchema(BaseModel):

    services: List[ServicePublicSchema]

    class Config:
        from_attributes = True

