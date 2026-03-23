from typing import TYPE_CHECKING, List
from decimal import Decimal
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:

    from api.models import Company, Service


class Segment(Base):

    __tablename__ = "segments"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(255), nullable = False)
    contract: Mapped[str] = mapped_column(Text, nullable = True)
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
        back_populates = "segments"
    )

    services: Mapped[List["Service"]] = relationship(
        "Service",
        back_populates = "segment"
    )
