import pytz
from typing import Dict, List, Optional
from datetime import datetime
from api.models import Segment
from api.repositories import SegmentRepository, CompanyRepository
from api.schemas import SegmentSchema
from api.exceptions import (
    CompanyNotFound,
    SegmentNotFound,
    SegmentInvalidName,
    SegmentAccesDenied
)


class SegmentService:

    def __init__(
        self,
        segment_repository: SegmentRepository,
        company_repository: CompanyRepository
    ):
        self._segment_repository = segment_repository
        self._company_repository = company_repository

    async def create(self, segment_data: SegmentSchema) -> Segment:
        company = await self._company_repository.get_by_id(segment_data.company_id)

        if not company:
            raise CompanyNotFound()

        segment = Segment(
            name=segment_data.name,
            contract=segment_data.contract,
            company_id=segment_data.company_id
        )

        return await self._segment_repository.save(segment)

    async def list(
        self,
        company_id: int,
        offset: int,
        limit: int,
        search: Optional[str]
    ) -> List[Segment]:
        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFound()

        if search:
            search = f"%{search}%"

        return await self._segment_repository.get_by_company_id(
            company_id,
            offset,
            limit,
            search
        )

    async def get(self, company_id: int, segment_id: int) -> Segment:
        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFound()

        segment = await self._segment_repository.get_by_id(company_id, segment_id)

        if not segment:
            raise SegmentNotFound()

        return segment

    async def delete(self, company_id: int, segment_id: int) -> None:
        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFound()

        segment = await self._segment_repository.get_by_id(company_id, segment_id)

        if not segment:
            raise SegmentNotFound()

        await self._segment_repository.delete_by_id(company_id, segment_id)

    async def update(self, segment_id: int, segment_data: Dict) -> Segment:
        company = await self._company_repository.get_by_id(segment_data["company_id"])

        if not company:
            raise CompanyNotFound()

        segment = await self._segment_repository.get_by_id(
            segment_data["company_id"],
            segment_id
        )

        if not segment:
            raise SegmentNotFound()

        if "name" in segment_data and not segment_data["name"]:
            raise SegmentInvalidName()

        if "company_id" in segment_data and segment.company_id != segment_data["company_id"]:
            raise SegmentAccesDenied()

        _BRAZIL_TIMEZONE_ = pytz.timezone("America/Sao_Paulo")
        segment.name = segment_data["name"]
        segment.company_id = segment_data["company_id"]
        segment.contract = segment_data["contract"]
        segment.updated_at = datetime.now(_BRAZIL_TIMEZONE_)

        return await self._segment_repository.update(segment)
