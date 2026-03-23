from typing import TYPE_CHECKING, List
from enum import Enum
from decimal import Decimal
from datetime import datetime
from sqlalchemy import String, Float, ForeignKey, DateTime, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


from api.models import Base

if TYPE_CHECKING:

    from api.models import Company, User


class Employee(Base):

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(255), nullable = False)
    function_name: Mapped[str] = mapped_column(String(255), nullable = True)
    money: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )
    hours_per_month: Mapped[float] = mapped_column(Float, nullable = False)
    food_assistance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )
    transport_assistance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )
    others_benefits: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )
    health_plan: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )
    cost_per_minute: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete = "SET NULL"),
        nullable = True
    )
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companys.id", ondelete = "CASCADE"),
        nullable = False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default = func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        onupdate = func.now(),
        server_default = func.now()
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates = "employee"
    )

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates = "employees"
    )
