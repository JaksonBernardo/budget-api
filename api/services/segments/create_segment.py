from api.models import Segment
from api.repositories import SegmentRepository, CompanyRepository
from api.schemas import SegmentSchema
from api.services.segments.service import SegmentService

from api.exceptions import CompanyNotFound

class CreateSegmentService(SegmentService):

    def __init__(self, 
                 segment_repository: SegmentRepository,
                 company_repository: CompanyRepository,
                 segment_data: SegmentSchema):
        super().__init__(segment_repository)

        self._segment_data = segment_data
        self._company_repository = company_repository

    async def execute(self) -> Segment:

        company = await self._company_repository.get_by_id(self._segment_data.company_id)

        if not company:

            raise CompanyNotFound()
        
        segment_db = Segment(
            name = self._segment_data.name,
            contract = self._segment_data.contract,
            company_id = self._segment_data.company_id
        )

        new_segment = await self._segment_repository.save(segment_db)

        return new_segment

