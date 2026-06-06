from typing import TYPE_CHECKING, List
from decimal import Decimal
from enum import Enum
from datetime import datetime, date
from sqlalchemy import (
    DateTime, 
    String, 
    Numeric, 
    Text, 
    Date, 
    ForeignKey, 
    Integer, 
    func, 
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:

    from api.models import Company, Client, Service, Budget, StatusProject


class ProjectOrigin(str, Enum):
    BUDGET = "BUDGET"
    MANUAL = "MANUAL"
    IMPORT = "IMPORT"



class Project(Base):

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    budget_id: Mapped[int] = mapped_column(
        ForeignKey('budgets.id', ondelete = "SET NULL"),
        nullable = True
    )
    client_id: Mapped[int] = mapped_column(
        ForeignKey('clients.id', ondelete = "RESTRICT")
    )
    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    origin: Mapped[ProjectOrigin] = mapped_column(
        String(20),
        nullable = False,
        default = ProjectOrigin.MANUAL
    ) 
    campaign: Mapped[int] = mapped_column(Integer, nullable = True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companys.id", ondelete="CASCADE"),
        nullable=False
    )
    status_id: Mapped[int] = mapped_column(
        ForeignKey("status_projects.id", ondelete="SET NULL"),
        nullable = True
    )
    start_date: Mapped[date] = mapped_column(
        Date,
        nullable = False
    )
    estimated_end_date: Mapped[date] = mapped_column(
        Date,
        nullable = True
    )
    end_date: Mapped[date] = mapped_column(
        Date,
        nullable = True
    )
    notes: Mapped[str] = mapped_column(
        Text,
        nullable = True
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

    budget: Mapped["Budget"] = relationship(back_populates = "projects")
    client: Mapped["Client"] = relationship(back_populates = "projects")
    company: Mapped["Company"] = relationship(back_populates = "projects")
    status: Mapped["StatusProject"] = relationship(back_populates = "projects")
    services: Mapped[List["ProjectService"]] = relationship(
        back_populates = "project",
        cascade = "all, delete-orphan"
    )



class ProjectService(Base):

    __tablename__ = "project_services"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey('projects.id', ondelete = "CASCADE")
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey('services.id', ondelete = "SET NULL"),
        nullable = True
    )
    service_name: Mapped[str] = mapped_column(Text)
    service_qtd: Mapped[int]
    service_value: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable = False
    )
    service_total_value: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable = False
    )
    start_date: Mapped[date] = mapped_column(
        Date,
        default = None,
        nullable = True
    )
    delivery_date: Mapped[date] = mapped_column(
        Date,
        default = None,
        nullable = True
    )

    project: Mapped["Project"] = relationship(back_populates = "services")
    service: Mapped["Service"] = relationship(back_populates = "project_services")

    __table_args__ = (
        CheckConstraint(
            "service_qtd > 0",
            name="check_project_service_qtd_positive"
        ),
        CheckConstraint(
            "service_value >= 0",
            name="check_project_service_value_positive"
        ),
        CheckConstraint(
            "service_total_value >= 0",
            name="check_project_service_total_positive"
        )
    )
