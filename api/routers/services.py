from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import (
    CompanyNotFound,
    SegmentNotFound,
    PriceNotFound,
    MaterialNotFound,
    EmployeeNotFound
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import (
    CompanyRepository,
    SegmentRepository,
    PriceRepository,
    MaterialRepository,
    EmployeeRepository,
    PrecificationServiceRepository
)
from api.core.database import get_session
from api.schemas import (
    ServiceSchema,
    ServicePriceSchema,
    ServicePublicSchema,
    ServiceEmployeeSchema,
    ServiceMaterialSchema,
    ServiceEmployeeSchema,
    ServicePublicPriceSchema,
    ServicePublicEmployeeSchema,
    ServicePublicMaterialSchema,
)
from api.services.precifications import PrecificationService
from api.security.dependencies import CurrentUser

segment_router = APIRouter(
    prefix = "/api/v1/services",
    tags = ["Services"]
)




