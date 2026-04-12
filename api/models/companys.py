from typing import TYPE_CHECKING, List
from enum import Enum
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:

    from api.models import (
        Plan,
        User,
        Client,
        Supplier,
        Material,
        Employee,
        Price,
        Segment,
        Service
    )

class State(str, Enum):
    AC = "AC"
    AL = "AL"
    AM = "AM"
    AP = "AP"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MG = "MG"
    MS = "MS"
    MT = "MT"
    PA = "PA"
    PB = "PB"
    PE = "PE"
    PI = "PI"
    PR = "PR"
    RJ = "RJ"
    RN = "RN"
    RO = "RO"
    RR = "RR"
    RS = "RS"
    SC = "SC"
    SE = "SE"
    SP = "SP"
    TO = "TO"

class Company(Base):

    __tablename__ = "companys"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    customer_id: Mapped[str] = mapped_column(String(255), unique = True, nullable = True)
    photo: Mapped[str] = mapped_column(String(255), nullable = True)
    email: Mapped[str] = mapped_column(String(255), unique = True)
    name: Mapped[str] = mapped_column(String(255), nullable = False)
    address: Mapped[str] = mapped_column(String(255), nullable = True)
    number: Mapped[int] = mapped_column(Integer, nullable = True)
    state: Mapped[State] = mapped_column(String(2), nullable = True)
    cep: Mapped[int] = mapped_column(Integer, nullable = True)
    city: Mapped[str] = mapped_column(String(255), nullable = True)
    cnpj: Mapped[str] = mapped_column(String(255), nullable = False)
    phone: Mapped[str] = mapped_column(String(255), nullable = True)
    whatsapp: Mapped[str] = mapped_column(String(255), nullable = True)
    website: Mapped[str] = mapped_column(String(255), nullable = True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default = False)
    plan_id: Mapped[int] = mapped_column(
        ForeignKey("plans.id", ondelete = "SET NULL", onupdate = "SET NULL"),
        nullable = True
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

    plan: Mapped["Plan"] = relationship(
        "Plan",
        back_populates = "companys"
    )

    users: Mapped[List["User"]] = relationship(
        "User",
        back_populates = "company"
    )

    clients: Mapped[List["Client"]] = relationship(
        "Client",
        back_populates = "company"
    )

    suppliers: Mapped[List["Supplier"]] = relationship(
        "Supplier",
        back_populates = "company"
    )

    materials: Mapped[List["Material"]] = relationship(
        "Material",
        back_populates = "company"
    )

    employees: Mapped[List["Employee"]] = relationship(
        "Employee",
        back_populates = "company"
    )

    prices: Mapped[List["Price"]] = relationship(
        "Price",
        back_populates = "company"
    )

    segments: Mapped[List["Segment"]] = relationship(
        "Segment",
        back_populates = "company"
    )

    services: Mapped[List["Service"]] = relationship(
        "Service",
        back_populates = "company"
    )
