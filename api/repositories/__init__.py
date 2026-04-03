from api.repositories.segments import SegmentRepository
from api.repositories.companys import CompanyRepository
from api.repositories.clients import ClientRepository
from api.repositories.legal_entity import LegalEntityRepository
from api.repositories.suppliers import SupplierRepository
from api.repositories.materials import MaterialRepository
from api.repositories.users import UserRepository

__all__ = [
    "SegmentRepository",
    "CompanyRepository",
    "ClientRepository",
    "LegalEntityRepository",
    "SupplierRepository",
    "MaterialRepository",
    "UserRepository"
]