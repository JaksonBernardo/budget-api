from api.models import Segment
from api.repositories import SegmentRepository, CompanyRepository
from api.services.segments.service import SegmentService

from api.exceptions import CompanyNotFound, SegmentNotFound

class GetSegmentService(SegmentService):

    def __init__(self, 
                 segment_repository: SegmentRepository,
                 company_repository: CompanyRepository,
                 company_id: int,
                 segment_id: int):
        super().__init__(segment_repository)

        self._company_id = company_id
        self._segment_id = segment_id
        self._company_repository = company_repository

    async def execute(self) -> Segment:

        company = await self._company_repository.get_by_id(
            self._company_id
        )

        if not company:

            raise CompanyNotFound()
        
        segment = await self._segment_repository.get_by_id(
            self._company_id,
            self._segment_id
        )

        if not segment:

            raise SegmentNotFound()

        return segment