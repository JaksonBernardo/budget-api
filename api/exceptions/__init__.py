from api.exceptions.companys import ZeroCompanyId, InvalidTypeCompanyId, CompanyNotFound
from api.exceptions.segments import SegmentInvalidName, SegmentNotFound, SegmentAccesDenied

__all__ = [
    "ZeroCompanyId",
    "InvalidTypeCompanyId",
    "CompanyNotFound",
    "SegmentInvalidName",
    "SegmentNotFound",
    "SegmentAccesDenied"
]
