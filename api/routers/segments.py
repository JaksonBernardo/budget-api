from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import (
    CompanyNotFound, 
    SegmentInvalidName,
    SegmentNotFound,
    SegmentAccesDenied
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import SegmentRepository, CompanyRepository
from api.core.database import get_session
from api.schemas import (
    SegmentSchema,
    SegmentPublicSchema,
    ListSegmentPublicSchema,
    SegmentUpdateSchema
)
from api.services.segments.create_segment import CreateSegmentService
from api.services.segments.list_segments import ListSegmentService
from api.services.segments.get_segment import GetSegmentService
from api.services.segments.delete_segment import DeleteSegmentService
from api.services.segments.update_segment import UpdateSegmentService

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
    company_repository: CompanyRepository = Depends(get_company_repository),
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


@segment_router.get(
    path = "/{company_id}",
    status_code = status.HTTP_200_OK,
    summary = "Listando todos os segmentos",
    response_model = ListSegmentPublicSchema
)
async def list_segments(
    company_id: int,
    segment_repository: SegmentRepository = Depends(get_segment_repository),
    company_repository: CompanyRepository = Depends(get_company_repository),
    offset: int = Query(0, ge = 0, description = "Registros a serem pulados"),
    limit: int = Query(20, ge = 1, description = "Qtd máxima de registros apresentados"),
    search: Optional[str] = Query(None, description = "Pesquisar pelo nome de algum segmento")
):
    
    try:

        segments = await ListSegmentService(
            segment_repository,
            company_repository,
            company_id,
            offset,
            limit,
            search
        ).execute()

        return {
            "segments": segments
        }
    
    except CompanyNotFound as e:
        raise map_exception(e)


@segment_router.get(
    path = "/{company_id}/{segment_id}",
    status_code = status.HTTP_200_OK,
    summary = "Selecionando um segmento específico",
    response_model = SegmentPublicSchema
)
async def get_segment(
    company_id: int,
    segment_id: int,
    segment_repository: SegmentRepository = Depends(get_segment_repository),
    company_repository: CompanyRepository = Depends(get_company_repository),
):
    
    try:

        segment = await GetSegmentService(
            segment_repository,
            company_repository,
            company_id,
            segment_id
        ).execute()

        return segment
    
    except (CompanyNotFound, SegmentNotFound) as e:
        raise map_exception(e)


@segment_router.delete(
    path = "/{company_id}/{segment_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Deletando um segmento específico"
)
async def delete_segment(
    company_id: int,
    segment_id: int,
    segment_repository: SegmentRepository = Depends(get_segment_repository),
    company_repository: CompanyRepository = Depends(get_company_repository),
):
    
    try:

        await DeleteSegmentService(
            segment_repository,
            company_repository,
            company_id,
            segment_id
        ).execute()

    except (CompanyNotFound, SegmentNotFound) as e:
        raise map_exception(e)
    

@segment_router.put(
    path = "/{segment_id}",
    status_code = status.HTTP_200_OK,
    summary = "Atualizando um segmento",
    response_model = SegmentPublicSchema
)
async def update_segment(
    segment_id: int,
    segment_data: SegmentUpdateSchema,
    segment_repository: SegmentRepository = Depends(get_segment_repository),
    company_repository: CompanyRepository = Depends(get_company_repository),
):
    
    try:

        segment_info = segment_data.model_dump(exclude_unset = True)

        segment = await UpdateSegmentService(
            segment_repository,
            company_repository,
            segment_id,
            segment_info
        ).execute()

        return segment

    except (CompanyNotFound, SegmentNotFound, SegmentAccesDenied, SegmentInvalidName) as e:
        raise map_exception(e)

