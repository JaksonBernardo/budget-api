from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import date, datetime


class StatusBudgetSchema(BaseModel):

    name: str
    color: str
    is_sale: bool = False
    company_id: int



class StatusBudgetPublicSchema(BaseModel):

    id: int
    name: str
    color: str
    is_sale: bool = False
    company_id: int
    created_at: datetime
    updated_at: datetime


class StatusBudgetUpdateSchema(BaseModel):

    name: Optional[str]
    color: Optional[str]
    is_sale: Optional[bool] = False
    company_id: int


class ListStatusBudgetPublicSchema(BaseModel):

    status: List[StatusBudgetPublicSchema]
    offset: int
    limit: int



