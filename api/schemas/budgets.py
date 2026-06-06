from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import date, datetime

from api.models import TypeDiscount


class BudgetServicesSchema(BaseModel):

    service_id: int
    price_id: int
    qtd: int
    service_value: Decimal = Field(ge = 0, max_digits = 12, decimal_places = 2)


class BudgetServicesPublicSchema(BudgetServicesSchema):

    total_value: Decimal = Field(ge = 0, max_digits = 12, decimal_places = 2)


class BudgetSchema(BaseModel):

    client_id: int
    user_id: int
    validity_date: date
    date_acceptance: date
    date_starter_services: date
    status_id: int
    payment_condition: int
    type_discount: TypeDiscount
    value_discount: Decimal = Field(ge = 0, max_digits = 12, decimal_places = 2)
    company_id: int

    services: List[BudgetServicesSchema]


class BudgetUpdateSchema(BaseModel):

    client_id: Optional[int] = None
    user_id: Optional[int] = None
    validity_date: Optional[date] = None
    date_acceptance: Optional[date] = None
    date_starter_services: Optional[date] = None
    status_id: Optional[int] = None
    payment_condition: Optional[int] = None
    type_discount: Optional[TypeDiscount] = None
    value_discount: Optional[Decimal] = Field(None, ge = 0, max_digits = 12, decimal_places = 2)

    services: Optional[List[BudgetServicesSchema]] = None


class BudgetPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    user_id: int
    validity_date: date
    date_acceptance: date
    date_starter_services: date
    status_id: int
    payment_condition: int
    type_discount: TypeDiscount
    value_discount: Decimal = Field(ge = 0, max_digits = 12, decimal_places = 2)
    total_value: Decimal = Field(ge = 0, max_digits = 12, decimal_places = 2)
    company_id: int
    created_at: datetime
    updated_at: datetime

    services: List[BudgetServicesPublicSchema] = []


class BudgetUpdateStatusSchema(BaseModel):

    status_id: int

class ListBudgetPublicSchema(BaseModel):

    budgets: List[BudgetPublicSchema]
    limit: int
    offset: int
