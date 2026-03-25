from api.models import Segment
from api.repositories import SegmentRepository, CompanyRepository
from api.schemas import SegmentSchema
from api.services.segments.service import SegmentService

from api.exceptions import CompanyNotFound

class ListSegmentService(SegmentService):

    def __init__(self, 
                 segment_repository: SegmentRepository,
                 company_repository: CompanyRepository,
                 company_id: int):
        super().__init__(segment_repository)

        self._company_id = company_id
        self._company_repository = company_repository

    async def execute(self) -> Segment:

        company = await self._company_repository.get_by_id(
            self._company_id
        )

        if not company:

            raise CompanyNotFound()
        
        segments = await self._segment_repository.get_by_company_id(
            self._company_id
        )

        return segments

