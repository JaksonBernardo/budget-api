from api.models import Segment
from api.repositories import SegmentRepository


class SegmentService:

    def __init__(self, segment_repository: SegmentRepository):

        self._segment_repository = segment_repository


