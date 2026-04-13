from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, field_validator
from datetime import datetime, date

from api.models import (
    BillingType, 
    StatusSubscription, 
    PaymentCycle, 
    DiscountType
)

class SubscriptionPublicSchema(BaseModel):

    id: int
    subscription_id: str
    company_id: int
    plan_id: int
    billing_type: BillingType
    cycle: PaymentCycle
    value: Decimal
    start_date: date
    end_date: date
    description: Optional[str]
    status: StatusSubscription
    discount_value: Decimal
    discount_type: DiscountType
    created_at: datetime
    updated_at: datetime





