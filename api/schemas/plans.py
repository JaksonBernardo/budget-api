from typing import Optional, List
from decimal import Decimal

from pydantic import BaseModel, field_validator
from datetime import datetime

from api.exceptions.plans import (
    PlanInvalidName,
    PlanNegativePrice,
)

class PlanSchema(BaseModel):

    name: str
    description: Optional[str]
    price: Decimal

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):

        if not value:

            raise PlanInvalidName()
        
        return value


class PlanPublicSchema(BaseModel):

    id: int
    name: str
    description: Optional[str]
    price: Decimal
    created_at: datetime
    updated_at: datetime


class PlanUpdateSchema(BaseModel):

    name: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):

        if not value:

            raise PlanInvalidName()
        
        return value
    

class ListPlanPublicSchema(BaseModel):

    plans: List[PlanPublicSchema]
    limit: int
    offset: int

