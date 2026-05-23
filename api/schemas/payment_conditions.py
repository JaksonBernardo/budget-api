from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from enum import Enum

class BillingType(str, Enum):
    START_PROJECT = "START_PROJECT"
    END_PROJECT = "END_PROJECT"
    INSTALLMENT = "INSTALLMENT"

class PaymentInstallmentSchema(BaseModel):
    order: int
    percent: Decimal = Field(max_digits=5, decimal_places=2)
    days_after: int = 30

class PaymentInstallmentPublicSchema(PaymentInstallmentSchema):
    id: int
    payment_condition_id: int

    class Config:
        from_attributes = True

class PaymentConditionSchema(BaseModel):
    name: str = Field(..., max_length=255)
    billing_type: BillingType = BillingType.END_PROJECT
    company_id: int
    installments: List[PaymentInstallmentSchema] = []

class PaymentConditionUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    billing_type: Optional[BillingType] = None
    company_id: int
    installments: Optional[List[PaymentInstallmentSchema]] = None

class PaymentConditionPublicSchema(BaseModel):
    id: int
    name: str
    billing_type: BillingType
    company_id: int
    installments: List[PaymentInstallmentPublicSchema]

    class Config:
        from_attributes = True

class ListPaymentConditionPublicSchema(BaseModel):
    payment_conditions: List[PaymentConditionPublicSchema]
    limit: int
    offset: int
