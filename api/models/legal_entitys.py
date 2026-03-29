from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base
from api.models.companys import State

if TYPE_CHECKING:
    from api.models import (
        Company,
        Material
    )


class LegalEntity(Base):

    __tablename__ = "person_entitys"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    companie: Mapped[str] = mapped_column(String(255), nullable = False)
    cpf_cnpj: Mapped[str] = mapped_column(String(255), nullable = True)
    email: Mapped[str] = mapped_column(String(255), nullable = True, unique = True)
    phone: Mapped[str] = mapped_column(String(50), nullable = True)
    address: Mapped[str] = mapped_column(String(255), nullable = True)
    number: Mapped[int] = mapped_column(Integer, nullable = True, default = None)
    state: Mapped[State] = mapped_column(String(2), nullable = True)
    cep: Mapped[str] = mapped_column(String(30), nullable = True)
    city: Mapped[str] = mapped_column(String(100), nullable = True)

    clients: Mapped[Optional["Client"]] = relationship(
        "Client",
        back_populates="legal_entity",
        uselist=False
    )
    suppliers: Mapped[Optional["Supplier"]] = relationship(
        "Supplier",
        back_populates="legal_entity",
        uselist=False
    )


class Client(Base):

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    id_person: Mapped[int] = mapped_column(
        ForeignKey("person_entitys.id", ondelete = "CASCADE"),
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
        server_default = func.now(),
        onupdate = func.now()
    )

    legal_entity: Mapped["LegalEntity"] = relationship(
        "LegalEntity",
        back_populates = "clients"
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

    legal_entity: Mapped["LegalEntity"] = relationship(
        "LegalEntity",
        back_populates = "suppliers"
    )

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates = "suppliers"
    )

    materials: Mapped[List["Material"]] = relationship(
        "Material",
        back_populates = "supplier"
    )

