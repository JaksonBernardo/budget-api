from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, field_validator, model_validator
from api.exceptions.prices import (
    PriceInvalidName,
    PriceInvalidValue,
    PriceExceedValue
)
from api.exceptions.companys import (
    InvalidTypeCompanyId,
    ZeroCompanyId
)

class PriceSchema(BaseModel):
    name: str
    fixed_expenses: Decimal
    impost: Decimal
    commission: Decimal
    others_rates: Decimal
    profit_margin: Decimal
    markup: Decimal
    company_id: int

    @field_validator("name")
    def validate_name(cls, value):
        if not isinstance(value, str):
            raise TypeError("Name tem que ser do tipo string")
        if not value.strip():
            raise PriceInvalidName()
        return value

    @model_validator(mode = "after")
    def validate_rates(self):
        rates = [
            self.fixed_expenses,
            self.impost,
            self.commission,
            self.others_rates,
            self.profit_margin
        ]
        
        if any(rate < 0 for rate in rates):
            raise PriceInvalidValue()
        
        if sum(rates) >= 100:
            raise PriceExceedValue()
            
        return self

    @field_validator("company_id")
    def validate_company_id(cls, value):
        if not isinstance(value, int):
            raise InvalidTypeCompanyId()
        if value <= 0:
            raise ZeroCompanyId()
        return value

class PricePublicSchema(BaseModel):
    id: int
    name: str
    fixed_expenses: Decimal
    impost: Decimal
    commission: Decimal
    others_rates: Decimal
    profit_margin: Decimal
    markup: Decimal
    company_id: int

class PriceUpdateSchema(BaseModel):
    name: Optional[str] = None
    fixed_expenses: Optional[Decimal] = None
    impost: Optional[Decimal] = None
    commission: Optional[Decimal] = None
    others_rates: Optional[Decimal] = None
    profit_margin: Optional[Decimal] = None
    markup: Optional[Decimal] = None

    @field_validator("name")
    def validate_name(cls, value):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError("Name tem que ser do tipo string")
            if not value.strip():
                raise PriceInvalidName()
        return value

    @model_validator(mode = "after")
    def validate_rates(self):
        # Only validate if at least one rate is being updated
        # This is a bit tricky for partial updates if we don't have the current values
        # But usually we'd want to ensure the final state is valid.
        # For simple CRUD, we can just check the provided ones are non-negative.
        rates = [
            self.fixed_expenses,
            self.impost,
            self.commission,
            self.others_rates,
            self.profit_margin
        ]
        
        if any(rate is not None and rate < 0 for rate in rates):
            raise PriceInvalidValue()
            
        return self

class ListPricePublicSchema(BaseModel):
    prices: List[PricePublicSchema]
