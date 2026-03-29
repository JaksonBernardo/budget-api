from api.exceptions.companys import ZeroCompanyId, InvalidTypeCompanyId, CompanyNotFound
from api.exceptions.segments import SegmentInvalidName, SegmentNotFound, SegmentAccesDenied
from api.exceptions.clients import ClientNotFound, ClientAccesDenied
from api.exceptions.suppliers import SupplierNotFound, SupplierAccesDenied

__all__ = [
    "ZeroCompanyId",
    "InvalidTypeCompanyId",
    "CompanyNotFound",
    "SegmentInvalidName",
    "SegmentNotFound",
    "SegmentAccesDenied",
    "ClientNotFound",
    "ClientAccesDenied",
    "SupplierNotFound",
    "SupplierAccesDenied"
]
