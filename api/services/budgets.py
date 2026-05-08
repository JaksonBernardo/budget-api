import pytz
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import (
    Budget,
    BudgetService
)
from api.repositories import (
    CompanyRepository,
    PrecificationServiceRepository,
    ClientRepository,
    UserRepository,
    BudgetRepository,
    BudgetServiceRepository
)
from api.schemas import (
    BudgetPublicSchema,
    BudgetSchema,
    BudgetServicesSchema
)
from api.exceptions import (
    CompanyNotFound,
    ServiceNotFound,
    ClientNotFound,
    UserNotFound,
)



class BudgetService:

    def __init__(
        self,
        company_repository: CompanyRepository,
        precification_repository: PrecificationServiceRepository,
        client_repository: ClientRepository,
        user_repository: UserRepository,
        budget_repository: BudgetRepository,
        budget_service_repository: BudgetServiceRepository
    ) -> None:
        
        self.__company_repository = company_repository
        self.__precification_repository = precification_repository
        self.__client_repository = client_repository
        self.__user_repository = user_repository
        self.__budget_repository = budget_repository
        self.__budget_service_repository = budget_service_repository





