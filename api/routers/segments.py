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
from api.services.segments import SegmentService
from api.security.dependencies import CurrentUser

segment_router = APIRouter(
    prefix = "/api/v1/segments",
    tags = ["Segments"]
)

def get_segment_repository(db: AsyncSession = Depends(get_session)) -> SegmentRepository:
    return SegmentRepository(db)

def get_company_repository(db: AsyncSession = Depends(get_session)) -> CompanyRepository:
    return CompanyRepository(db)

def get_segment_service(
    segment_repository: SegmentRepository = Depends(get_segment_repository),
    company_repository: CompanyRepository = Depends(get_company_repository)
) -> SegmentService:
    return SegmentService(segment_repository, company_repository)


@segment_router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Criando um segmento",
    response_model = SegmentPublicSchema
)
async def create_segment(
    segment_data: SegmentSchema,
    service: SegmentService = Depends(get_segment_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        new_segment = await service.create(segment_data)
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
    service: SegmentService = Depends(get_segment_service),
    current_user: CurrentUser = CurrentUser,
    offset: int = Query(0, ge = 0, description = "Registros a serem pulados"),
    limit: int = Query(20, ge = 1, le = 100, description = "Qtd máxima de registros apresentados"),
    search: Optional[str] = Query(None, description = "Pesquisar pelo nome de algum segmento")
):
    try:
        segments = await service.list(company_id, offset, limit, search)
        return {
            "segments": segments,
            "limit": limit,
            "offset": offset
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
    service: SegmentService = Depends(get_segment_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        segment = await service.get(company_id, segment_id)
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
    service: SegmentService = Depends(get_segment_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        await service.delete(company_id, segment_id)

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
    service: SegmentService = Depends(get_segment_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        segment_info = segment_data.model_dump(exclude_unset = True)
        segment = await service.update(segment_id, segment_info)
        return segment

    except (CompanyNotFound, SegmentNotFound, SegmentAccesDenied, SegmentInvalidName) as e:
        raise map_exception(e)
