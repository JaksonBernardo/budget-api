from typing import TYPE_CHECKING
from enum import Enum
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:

    from api.models import Company


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(255), nullable = False)
    email: Mapped[str] = mapped_column(String(255), nullable = False, unique = True)
    whatsapp: Mapped[str] = mapped_column(String(255), nullable = True)
    password: Mapped[str] = mapped_column(String(255), nullable = False)
    photo: Mapped[str] = mapped_column(String(255), nullable = True)
    profile: Mapped[int]
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companys.id")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable = True)

    company: Mapped["Company"] = relationship(
        "Company", 
        back_populates = "users"
    )


