from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import (
    CompanyNotFound,
    ServiceNotFound,
    ClientNotFound,
    UserNotFound,
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import (
    CompanyRepository,
    PrecificationServiceRepository,
    ClientRepository,
    UserRepository,
    BudgetRepository,
    BudgetServiceRepository
)
from api.core.database import get_session
from api.schemas import (
    BudgetServicesSchema,
    BudgetPublicSchema,
    BudgetSchema
)

from api.security.dependencies import CurrentUser




