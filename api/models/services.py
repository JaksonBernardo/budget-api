from typing import TYPE_CHECKING, List
from decimal import Decimal
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:

    from api.models import (
        Company,
        Material,
        Employee,
        Price,
        Segment
    )


class Service(Base):

    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(255), nullable = False)
    segment_id: Mapped[int] = mapped_column(
        ForeignKey("segments.id", ondelete = "SET NULL", onupdate = "CASCADE"),
        nullable = True
    )
    description: Mapped[str] = mapped_column(Text, nullable = True, default = None)
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
        back_populates = "services"
    )

    segment: Mapped["Segment"] = relationship(
        "Segment",
        back_populates = "services"
    )

    materials: Mapped[List["ServiceMaterial"]] = relationship(
        "ServiceMaterial",
        back_populates = "service"
    )

    employees: Mapped[List["ServiceEmployee"]] = relationship(
        "ServiceEmployee",
        back_populates = "service"
    )

    prices: Mapped[List["ServicePrice"]] = relationship(
        "ServicePrice",
        back_populates = "service"
    )


class ServiceMaterial(Base):

    __tablename__ = "services_materials"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete = "CASCADE"),
        nullable = False
    )
    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id", ondelete = "CASCADE"),
        nullable = False
    )
    qtd_material: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )
    total_cost: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )

    service: Mapped["Service"] = relationship(
        "Service",
        back_populates = "materials"
    )

    material: Mapped["Material"] = relationship(
        "Material",
        back_populates = "services"
    )


class ServiceEmployee(Base):

    __tablename__ = "services_employees"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete = "CASCADE"),
        nullable = False
    )
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete = "CASCADE"),
        nullable = False
    )
    minute_works: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )
    total_cost: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )

    service: Mapped["Service"] = relationship(
        "Service",
        back_populates = "employees"
    )

    employee: Mapped["Employee"] = relationship(
        "Employee",
        back_populates = "services"
    )


class ServicePrice(Base):

    __tablename__ = "services_prices"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete = "CASCADE"),
        nullable = False
    )
    price_id: Mapped[int] = mapped_column(
        ForeignKey("prices.id", ondelete = "CASCADE"),
        nullable = False
    )
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
    value: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )
    
    service: Mapped["Service"] = relationship(
        "Service",
        back_populates = "prices"
    )

    price: Mapped["Price"] = relationship(
        "Price",
        back_populates = "services"
    )


