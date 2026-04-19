from typing import Optional, List
from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from decimal import Decimal

from api.exceptions.employees import EmployeeInvalidData
from api.exceptions.companys import InvalidTypeCompanyId, ZeroCompanyId

class EmployeeSchema(BaseModel):
    name: str
    function_name: Optional[str] = None
    money: Decimal
    hours_per_month: float
    food_assistance: Decimal
    transport_assistance: Decimal
    others_benefits: Decimal
    health_plan: Decimal
    cost_per_minute: Decimal
    user_id: Optional[int] = None
    company_id: int

    @field_validator("name")
    def validate_name(cls, value):
        if not value:
            raise EmployeeInvalidData("Nome do colaborador não pode ser vazio")
        return value

    @field_validator("company_id")
    def validate_company_id(cls, value):
        if not isinstance(value, int):
            raise InvalidTypeCompanyId()
        if value <= 0:
            raise ZeroCompanyId()
        return value

class EmployeePublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    function_name: Optional[str]
    money: Decimal
    hours_per_month: float
    food_assistance: Decimal
    transport_assistance: Decimal
    others_benefits: Decimal
    health_plan: Decimal
    cost_per_minute: Decimal
    user_id: Optional[int]
    company_id: int
    created_at: datetime
    updated_at: datetime

class EmployeeUpdateSchema(BaseModel):
    name: Optional[str] = None
    function_name: Optional[str] = None
    money: Optional[Decimal] = None
    hours_per_month: Optional[float] = None
    food_assistance: Optional[Decimal] = None
    transport_assistance: Optional[Decimal] = None
    others_benefits: Optional[Decimal] = None
    health_plan: Optional[Decimal] = None
    cost_per_minute: Optional[Decimal] = None
    user_id: Optional[int] = None
    company_id: Optional[int] = None

    @field_validator("company_id")
    def validate_company_id(cls, value):
        if value is not None:
            if not isinstance(value, int):
                raise InvalidTypeCompanyId()
            if value <= 0:
                raise ZeroCompanyId()
        return value

class ListEmployeePublicSchema(BaseModel):
    employees: List[EmployeePublicSchema]
