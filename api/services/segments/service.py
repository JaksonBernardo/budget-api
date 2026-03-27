import pytz
from typing import Dict, Optional
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

    def __init__(self, segment_repository: SegmentRepository):
        self._segment_repository = segment_repository


class CreateSegmentService(SegmentService):

    def __init__(
        self,
        segment_repository: SegmentRepository,
        company_repository: CompanyRepository,
        segment_data: SegmentSchema
    ):
        super().__init__(segment_repository)
        self._segment_data = segment_data
        self._company_repository = company_repository

    async def execute(self) -> Segment:
        company = await self._company_repository.get_by_id(self._segment_data.company_id)

        if not company:
            raise CompanyNotFound()

        segment_db = Segment(
            name=self._segment_data.name,
            contract=self._segment_data.contract,
            company_id=self._segment_data.company_id
        )

        new_segment = await self._segment_repository.save(segment_db)
        return new_segment


class ListSegmentService(SegmentService):

    def __init__(
        self,
        segment_repository: SegmentRepository,
        company_repository: CompanyRepository,
        company_id: int,
        offset: int,
        limit: int,
        search: str
    ):
        super().__init__(segment_repository)
        self._company_id = company_id
        self._offset = offset
        self._limit = limit
        self._search = search
        self._company_repository = company_repository

    async def execute(self):
        company = await self._company_repository.get_by_id(self._company_id)

        if not company:
            raise CompanyNotFound()

        if self._search:
            self._search = f"%{self._search}%"

        segments = await self._segment_repository.get_by_company_id(
            self._company_id,
            self._offset,
            self._limit,
            self._search
        )

        return segments


class GetSegmentService(SegmentService):

    def __init__(
        self,
        segment_repository: SegmentRepository,
        company_repository: CompanyRepository,
        company_id: int,
        segment_id: int
    ):
        super().__init__(segment_repository)
        self._company_id = company_id
        self._segment_id = segment_id
        self._company_repository = company_repository

    async def execute(self) -> Segment:
        company = await self._company_repository.get_by_id(self._company_id)

        if not company:
            raise CompanyNotFound()

        segment = await self._segment_repository.get_by_id(
            self._company_id,
            self._segment_id
        )

        if not segment:
            raise SegmentNotFound()

        return segment


class DeleteSegmentService(SegmentService):

    def __init__(
        self,
        segment_repository: SegmentRepository,
        company_repository: CompanyRepository,
        company_id: int,
        segment_id: int
    ):
        super().__init__(segment_repository)
        self._company_id = company_id
        self._segment_id = segment_id
        self._company_repository = company_repository

    async def execute(self) -> Segment:
        company = await self._company_repository.get_by_id(self._company_id)

        if not company:
            raise CompanyNotFound()

        segment = await self._segment_repository.get_by_id(
            self._company_id,
            self._segment_id
        )

        if not segment:
            raise SegmentNotFound()

        await self._segment_repository.delete_by_id(
            self._company_id,
            self._segment_id
        )


class UpdateSegmentService(SegmentService):

    def __init__(
        self,
        segment_repository: SegmentRepository,
        company_repository: CompanyRepository,
        segment_id: int,
        segment_data: Dict
    ):
        super().__init__(segment_repository)
        self._segment_id = segment_id
        self._segment_data = segment_data
        self._company_repository = company_repository

    async def execute(self) -> Segment:
        company = await self._company_repository.get_by_id(self._segment_data["company_id"])

        if not company:
            raise CompanyNotFound()

        segment = await self._segment_repository.get_by_id(
            self._segment_data["company_id"],
            self._segment_id
        )

        if not segment:
            raise SegmentNotFound()

        if "name" in self._segment_data and not self._segment_data["name"]:
            raise SegmentInvalidName()

        if "company_id" in self._segment_data and segment.company_id != self._segment_data["company_id"]:
            raise SegmentAccesDenied()

        _BRAZIL_TIMEZONE_ = pytz.timezone("America/Sao_Paulo")
        segment.name = self._segment_data["name"]
        segment.company_id = self._segment_data["company_id"]
        segment.contract = self._segment_data["contract"]
        segment.updated_at = datetime.now(_BRAZIL_TIMEZONE_)

        segment = await self._segment_repository.update(segment)
        return segment
