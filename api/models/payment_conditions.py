from typing import TYPE_CHECKING, List
from enum import Enum
from decimal import Decimal
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:

    from api.models import (
        Company,
        Budget
    )


class BillingType(str, Enum):
    START_PROJECT = "START_PROJECT"
    END_PROJECT = "END_PROJECT"
    INSTALLMENT = "INSTALLMENT"


class PaymentCondition(Base):

    __tablename__ = "payment_conditions"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(255), nullable = False)
    billing_type: Mapped[BillingType] = mapped_column(
        String(50), nullable = False, default = "END_PROJECT"
    )
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companys.id", ondelete = "CASCADE")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default = func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default = func.now(),
        onupdate = func.now()
    )

    company: Mapped["Company"] = relationship(back_populates = "payment_conditions")
    installments: Mapped[List["PaymentInstallment"]] = relationship(
        back_populates = "payment_condition",
        cascade = "all, delete-orphan"
    )
    budgets: Mapped[List["Budget"]] = relationship(back_populates = "payment_condition_rel")


class PaymentInstallment(Base):

    __tablename__ = "payment_installments"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    payment_condition_id: Mapped[int] = mapped_column(
        ForeignKey("payment_conditions.id", ondelete = "CASCADE")
    )
    order: Mapped[int]
    percent: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    days_after: Mapped[int] = mapped_column(Integer, default = 30)

    payment_condition: Mapped["PaymentCondition"] = relationship(back_populates = "installments")






