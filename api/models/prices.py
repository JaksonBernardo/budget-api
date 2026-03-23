from typing import TYPE_CHECKING, List
from decimal import Decimal
from datetime import datetime
from sqlalchemy import String, Numeric, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:

    from api.models import Company, ServicePrice


class Price(Base):

    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(255), nullable = False)
    fixed_expenses: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable = False
    )
    impost: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable = False
    )
    commission: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable = False
    )
    others_rates: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable = False
    )
    profit_margin: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable = False
    )
    markup: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable = False
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

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates = "prices"
    )

    services: Mapped[List["ServicePrice"]] = relationship(
        "ServicePrice",
        back_populates = "price"
    )


