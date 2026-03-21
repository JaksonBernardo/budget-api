from typing import TYPE_CHECKING, List, Optional
from enum import Enum
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Text, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:

    from api.models import Company

class Feature(Base):

    __tablename__ = "features"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(100), nullable = False)
    name: Mapped[str] = mapped_column(String(255), nullable = False)

    plans: Mapped[List["Plan"]] = relationship(
        secondary="plan_features",
        back_populates="features"
    )


class Plan(Base):

    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable = False)
    description: Mapped[str] = mapped_column(Text, nullable = True)
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        onupdate=func.now(),
        server_default=func.now()
    )

    features: Mapped[List["Feature"]] = relationship(
        secondary="plan_features",
        back_populates="plans"
    )

    companys: Mapped[List["Company"]] = relationship(
        "Company",
        back_populates = "plan"
    )


class PlanFeature(Base):

    __tablename__ = "plan_features"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement=True)
    plan_id: Mapped[int] = mapped_column(
        ForeignKey("plans.id", ondelete = "CASCADE", onupdate = "CASCADE")
    )
    feature_id: Mapped[int] = mapped_column(
        ForeignKey("features.id", ondelete = "CASCADE", onupdate = "CASCADE")
    )

    plan: Mapped["Plan"] = relationship(back_populates="features")
    feature: Mapped["Feature"] = relationship(back_populates="plans")

