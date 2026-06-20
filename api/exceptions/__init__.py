from api.exceptions.companys import ZeroCompanyId, InvalidTypeCompanyId, CompanyNotFound, InvalidNameCompany, CnpjAlreadyExists, NameAlreadyExists
from api.exceptions.segments import SegmentInvalidName, SegmentNotFound, SegmentAccesDenied
from api.exceptions.clients import ClientNotFound, ClientAccesDenied
from api.exceptions.suppliers import SupplierNotFound, SupplierAccesDenied, ZeroSupplierId
from api.exceptions.materials import MaterialInvalidName, MaterialNotFound
from api.exceptions.users import UserNotFound, UserAlreadyExists, UserAccessDenied, InvalidUserId
from api.exceptions.plans import PlanInvalidName, PlanNegativePrice, PlanNotFound, PlanAlreadyExists, PlanHaveCompanys
from api.exceptions.employees import EmployeeNotFound, EmployeeAccessDenied, EmployeeInvalidData
from api.exceptions.prices import PriceExceedValue, PriceInvalidName, PriceInvalidValue, PriceNotFound
from api.exceptions.services import ServiceAccesDenied, ServiceInvalidName, ServiceNotFound, ServicePriceNotFound
from api.exceptions.status_budgets import StatusBudgetInvalidName, StatusBudgetNotFound, StatusBudgetIsSaleAlreadyExists
from api.exceptions.status_projects import StatusProjectInvalidName, StatusProjectNotFound, StatusProjectIsCompletedAlreadyExists, StatusProjectAccesDenied
from api.exceptions.payment_conditions import (
    PaymentConditionInvalidName, 
    PaymentConditionNameAlreadyExists, 
    PaymentConditionNotFound,
    PaymentConditionAccesDenied,
    PaymentConditionAssociatedWithBudget
)
from api.exceptions.budgets import BudgetNotFound
from api.exceptions.projects import ProjectInvalidOs, ProjectNotFound, ProjectServiceNotFound

__all__ = [
    "ZeroCompanyId",
    "InvalidTypeCompanyId",
    "CompanyNotFound",
    "InvalidNameCompany",
    "CnpjAlreadyExists", 
    "NameAlreadyExists",
    "SegmentInvalidName",
    "SegmentNotFound",
    "SegmentAccesDenied",
    "ClientNotFound",
    "ClientAccesDenied",
    "SupplierNotFound",
    "SupplierAccesDenied",
    "ZeroSupplierId",
    "MaterialInvalidName",
    "MaterialNotFound",
    "UserNotFound",
    "UserAlreadyExists",
    "UserAccessDenied",
    "InvalidUserId",
    "PlanInvalidName", 
    "PlanNegativePrice", 
    "PlanNotFound",
    "PlanAlreadyExists",
    "PlanHaveCompanys",
    "EmployeeNotFound",
    "EmployeeAccessDenied",
    "EmployeeInvalidData",
    "PriceExceedValue", 
    "PriceInvalidName", 
    "PriceInvalidValue", 
    "PriceNotFound",
    "ServiceAccesDenied", 
    "ServiceInvalidName", 
    "ServiceNotFound",
    "ServicePriceNotFound",
    "StatusBudgetInvalidName",
    "StatusBudgetNotFound",
    "StatusBudgetIsSaleAlreadyExists",
    "StatusProjectInvalidName",
    "StatusProjectNotFound",
    "StatusProjectIsCompletedAlreadyExists",
    "StatusProjectAccesDenied",
    "PaymentConditionInvalidName", 
    "PaymentConditionNameAlreadyExists", 
    "PaymentConditionNotFound",
    "PaymentConditionAccesDenied",
    "PaymentConditionAssociatedWithBudget",
    "BudgetNotFound",
    "ProjectInvalidOs", 
    "ProjectNotFound",
    "ProjectServiceNotFound"
]
