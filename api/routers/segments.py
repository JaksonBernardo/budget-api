
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import CompanyNotFound, SegmentInvalidName
from api.exceptions.map_exceptions import map_exception
from api.repositories import SegmentRepository, CompanyRepository
from api.core.database import get_session
from api.schemas import (
    SegmentSchema,
    SegmentPublicSchema
)
from api.services.segments.create_segment import CreateSegmentService

segment_router = APIRouter(
    prefix = "/api/segments",
    tags = ["Segments"]
)

def get_segment_repository(db: AsyncSession = Depends(get_session)) -> SegmentRepository:

    return SegmentRepository(db)

def get_company_repository(db: AsyncSession = Depends(get_session)) -> CompanyRepository:

    return CompanyRepository(db)

@segment_router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Criando um segmento",
    response_model = SegmentPublicSchema
)
async def create_segment(
    segment_data: SegmentSchema,
    segment_repository: SegmentRepository = Depends(get_segment_repository),
    company_repository: CompanyRepository = Depends(get_company_repository)
):

    try:

        new_segment = await CreateSegmentService(
            segment_repository,
            company_repository,
            segment_data
        ).execute()

        return new_segment
    
    except (CompanyNotFound, SegmentInvalidName) as e:
        raise map_exception(e)

    
