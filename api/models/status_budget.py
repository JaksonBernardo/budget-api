from typing import TYPE_CHECKING, List
from decimal import Decimal
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:

    from api.models import (
        Company,
        Budget
    )


class StatusBudget(Base):

    __tablename__ = "status_budgets"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    color: Mapped[str] = mapped_column(String(100), nullable = False)
    is_sale: Mapped[bool] = mapped_column(Boolean, default = False)
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

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates = "status_budgets"
    )

    budgets: Mapped[List["Budget"]] = relationship(
        "Budget",
        back_populates = "status"
    )





