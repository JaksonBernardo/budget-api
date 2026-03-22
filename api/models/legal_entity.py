from typing import TYPE_CHECKING, List
from enum import Enum
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:

    from api.models import (
        State, Company
    )


class LegalEntity(Base):

    __tablename__ = "person_entitys"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    companie: Mapped[str] = mapped_column(String(255), nullable = False)
    cpf_cnpj: Mapped[str] = mapped_column(String(255), nullable = True)
    email: Mapped[str] = mapped_column(String(255), nullable = True, unique = True)
    phone: Mapped[str] = mapped_column(String(50), nullable = True)
    address: Mapped[str] = mapped_column(String(255), nullable = True)
    number: Mapped[int] = mapped_column(Integer, nullable = True)
    state: Mapped[State] = mapped_column(String(2), nullable = True)
    cep: Mapped[str] = mapped_column(String(30), nullable = True)
    city: Mapped[str] = mapped_column(String(100), nullable = True)

    is_clients: Mapped["Client"] = mapped_column(
        "Client",
        back_populates = "legal_entity"
    )
    is_suppliers: Mapped["Supplier"] = mapped_column(
        "Supplier",
        back_populates = "legal_entity"
    )


class Client(Base):

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    id_person: Mapped[int] = mapped_column(
        ForeignKey("person_entitys.id", ondelete = "CASCADE"),
        nullable = False
    )
    payment_days: Mapped[int]
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companys.id", ondelete = "CASCADE"),
        nullable = False
    )

    legal_entity: Mapped["LegalEntity"] = mapped_column(
        "LegalEntity",
        back_populates = "is_clients"
    )

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates = "clients"
    )


class Supplier(Base):

    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    id_person: Mapped[int] = mapped_column(
        ForeignKey("person_entitys.id", ondelete = "CASCADE"),
        nullable = False
    )
    receive_days: Mapped[int]
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companys.id", ondelete = "CASCADE"),
        nullable = False
    )

    legal_entity: Mapped["LegalEntity"] = mapped_column(
        "LegalEntity",
        back_populates = "is_suppliers"
    )

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates = "suppliers"
    )

