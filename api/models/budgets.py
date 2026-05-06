from typing import TYPE_CHECKING, List
from decimal import Decimal
from enum import Enum
from datetime import datetime, date
from sqlalchemy import (
    String, 
    ForeignKey, 
    DateTime, 
    Date, 
    Numeric, 
    func, 
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:

    from api.models import (
        Company,
        Client,
        Service,
        User
    )


class TypeDiscount(str, Enum):
    FIXED = "FIXED"
    PERCENTAGE = "PERCENTAGE"


class Budget(Base):

    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey('clients.id', ondelete = "RESTRICT"),
        nullable = False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete = "RESTRICT"),
        nullable = False
    )
    validity_date: Mapped[date] = mapped_column(Date, nullable = True)
    date_acceptance: Mapped[date] = mapped_column(Date, nullable = True)
    date_starter_services: Mapped[date] = mapped_column(Date, nullable = True)
    status_id: Mapped[int]
    payment_option: Mapped[int]
    type_discount: Mapped[TypeDiscount] = mapped_column(
        String(30), 
        nullable = False,
        default = "FIXED"
    )
    value_discount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable = False,
        default = 0.0
    )
    company_id: Mapped[int] = mapped_column(
        ForeignKey('companys.id', ondelete = "RESTRICT"),
        nullable = False
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

    client: Mapped["Client"] = relationship(back_populates = "budgets")
    user: Mapped["User"] = relationship(back_populates = "budgets")
    company: Mapped["Company"] = relationship(back_populates = "budgets")
    services: Mapped[List["BudgetService"]] = relationship(
        back_populates = "budget",
        cascade = "all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "value_discount >= 0", 
            name = "check_budget_value_discount_positive"
        ),
        CheckConstraint(
            "(validity_date IS NULL) OR (validity_date >= date_acceptance)", 
            name="check_validity_after_acceptance"
        ),
        CheckConstraint(
            "(date_starter_services IS NULL) OR (date_starter_services >= date_acceptance)", 
            name="check_starter_service_after_acceptance"
        )
    )

class BudgetService(Base):

    __tablename__ = "budget_services"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    budget_id: Mapped[int] = mapped_column(
        ForeignKey('budgets.id', ondelete = "CASCADE"),
        nullable = False
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey('services.id', ondelete = "RESTRICT"),
        nullable = False
    )
    qtd: Mapped[int]
    service_value: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable = False
    )
    total_value: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable = False
    )

    budget: Mapped["Budget"] = relationship(back_populates = "services")
    service: Mapped["Service"] = relationship(back_populates = "budget_services")

    __table_args__ = (
        CheckConstraint(
            "qtd > 0",
            name = "check_qtd_service_budget_positive"
        ),
        CheckConstraint(
            "service_value > 0",
            name = "check_service_value_budget_positive"
        ),
        CheckConstraint(
            "total_value > 0",
            name = "check_total_value_budget_positive"
        )
    )
