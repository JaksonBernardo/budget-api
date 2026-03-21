from typing import TYPE_CHECKING
from enum import Enum
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:

    from api.models import Plan

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
    photo: Mapped[str] = mapped_column(String(255), nullable = True)
    name: Mapped[str] = mapped_column(String(255), nullable = False)
    address: Mapped[str] = mapped_column(String(255), nullable = True)
    number: Mapped[int] = mapped_column(Integer, nullable=True)
    state: Mapped[State] = mapped_column(String(2), nullable = True)
    cnpj: Mapped[str] = mapped_column(String(255), nullable = True)
    phone: Mapped[str] = mapped_column(String(255), nullable = True)
    whatsapp: Mapped[str] = mapped_column(String(255), nullable = True)
    website: Mapped[str] = mapped_column(String(255), nullable = True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default = False)
    plan_id: Mapped[int] = mapped_column(
        ForeignKey("plans.id", ondelete = "SET NULL", onupdate = "SET NULL")
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

