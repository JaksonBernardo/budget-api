from typing import TYPE_CHECKING, List
from enum import Enum
from decimal import Decimal
from datetime import datetime
from sqlalchemy import (
    String, 
    Integer, 
    ForeignKey, 
    DateTime, 
    Numeric, 
    func,
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:

    from api.models import Company, ServiceMaterial

class Classificate(str, Enum):
    DIRECT = "DIRECT"
    INDIRECT = "INDIRECT"

class Material(Base):

    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(255), nullable = False)
    unit_cost: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )
    stock: Mapped[int] = mapped_column(Integer, default = 0)
    classification: Mapped[Classificate] = mapped_column(String(20), nullable = True, default = None)
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
        server_default = func.now(),
        onupdate = func.now()
    )

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates = "materials"
    )

    services: Mapped[List["ServiceMaterial"]] = relationship(
        "ServiceMaterial",
        back_populates = "material"
    )

    movementations: Mapped[List["Movementation"]] = relationship(
        "Movementation",
        back_populates = "material"
    )

    __table_args__ = (
        CheckConstraint("unit_cost >= 0", name = "ck_material_unit_cost_positive"),
        CheckConstraint("stock >= 0", name = "ck_material_stock_positive"),
    )


class Movementation(Base):

    __tablename__ = "movementations"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    qtd: Mapped[int]
    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id", ondelete = "SET NULL", onupdate = "SET NULL"),
        nullable = True
    )
    value: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )
    material_name: Mapped[str] = mapped_column(String(255), nullable = True)

    material: Mapped["Material"] = relationship(
        "Material",
        back_populates = "movementations"
    )

    entrys: Mapped[List["Entrys"]] = relationship(
        "Entrys",
        back_populates = "movementation"
    )

    exits: Mapped[List["Exits"]] = relationship(
        "Exits",
        back_populates = "movementation"
    )

    __table_args__ = (
        CheckConstraint("qtd > 0", name = "ck_movementation_qtd_positive"),
    )


class Entrys(Base):

    __tablename__ = "entrys"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    movementation_id: Mapped[int] = mapped_column(
        ForeignKey("movementations.id", ondelete = "CASCADE", onupdate = "CASCADE"),
        nullable = False
    )
    date: Mapped[datetime] = mapped_column(DateTime, nullable = False)

    movementation: Mapped["Movementation"] = relationship(
        "Movementation",
        back_populates = "entrys"
    )


class Exits(Base):

    __tablename__ = "exits"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    movementation_id: Mapped[int] = mapped_column(
        ForeignKey("movementations.id", ondelete = "CASCADE", onupdate = "CASCADE"),
        nullable = False
    )
    date: Mapped[datetime] = mapped_column(DateTime, nullable = False)

    movementation: Mapped["Movementation"] = relationship(
        "Movementation",
        back_populates = "exits"
    )


