from typing import TYPE_CHECKING, List
from decimal import Decimal
from enum import Enum
from datetime import datetime, date
from sqlalchemy import String, Text, ForeignKey, DateTime, Date, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:

    from api.models import Company, Plan


class BillingType(str, Enum):
    UNDEFINED = "UNDEFINED"
    BOLETO = "BOLETO"
    CREDIT_CARD = "CREDIT_CARD"
    PIX = "PIX"

class PaymentCycle(str, Enum):
    WEEKLY = "WEEKLY"
    BIWEEKLY = "BIWEEKLY"
    MONTHLY = "MONTHLY"
    BIMONTHLY = "BIMONTHLY"
    QUARTERLY = "QUARTERLY"
    SEMIANNUALLY = "SEMIANNUALLY"
    YEARLY = "YEARLY"

class StatusSubscription(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    INACTIVE = "INACTIVE"

class DiscountType(str, Enum):
    FIXED = "FIXED"
    PERCENTAGE = "PERCENTAGE"


class Subscription(Base):

    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    subscription_id: Mapped[str] = mapped_column(String(255), unique = True, nullable = True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey('companys.id', ondelete = "CASCADE")
    )
    plan_id: Mapped[int] = mapped_column(
        ForeignKey('plans.id', ondelete = "SET NULL"),
        nullable = True
    )
    billing_type: Mapped[BillingType] = mapped_column(String(50), nullable = False)
    cycle: Mapped[PaymentCycle] = mapped_column(String(50), nullable = False)
    value: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )
    start_date: Mapped[date] = mapped_column(
        Date, nullable = False
    )
    end_date: Mapped[date] = mapped_column(
        Date, nullable = False
    )
    description: Mapped[str] = mapped_column(Text, nullable = True)
    status: Mapped[StatusSubscription] = mapped_column(String(50), nullable = False)
    discount_value: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable = False
    )
    discount_type: Mapped[DiscountType] = mapped_column(String(30), nullable = False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default = func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default = func.now(),
        onupdate = func.now()
    )

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates = "subscriptions"
    )

    plan: Mapped["Plan"] = relationship(
        "Plan",
        back_populates = "subscriptions"
    )
