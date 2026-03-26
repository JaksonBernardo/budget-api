import pytz
from typing import Dict
from datetime import datetime
from api.models import Segment
from api.repositories import SegmentRepository, CompanyRepository
from api.services.segments.service import SegmentService

from api.exceptions import (
    CompanyNotFound,
    SegmentNotFound, 
    SegmentInvalidName,
    SegmentAccesDenied
)

class UpdateSegmentService(SegmentService):

    def __init__(self, 
                 segment_repository: SegmentRepository,
                 company_repository: CompanyRepository,
                 segment_id: int,
                 segment_data: Dict):
        super().__init__(segment_repository)

        self._segment_id = segment_id
        self._segment_data = segment_data
        self._company_repository = company_repository

    async def execute(self) -> Segment:

        company = await self._company_repository.get_by_id(self._segment_data["company_id"])

        if not company:

            raise CompanyNotFound()
        
        segment = await self._segment_repository.get_by_id(
            self._segment_data["company_id"], self._segment_id
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