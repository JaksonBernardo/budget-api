from typing import List, Optional, Dict
from datetime import datetime
import pytz

from api.models import Plan
from api.repositories import (
    PlanRepository,
    CompanyRepository
)
from api.schemas.plans import PlanSchema
from api.exceptions.plans import (
    PlanInvalidName,
    PlanNegativePrice,
    PlanNotFound,
    PlanAlreadyExists,
    PlanHaveCompanys
)


class PlanService:

    def __init__(
        self,
        plan_repository: PlanRepository,
    ):
        
        self.__plan_repository = plan_repository

    async def create(self, plan_data: PlanSchema) -> Plan:

        plan = await self.__plan_repository.verify_exists_by_name(
            plan_data.name
        )

        if plan:

            raise PlanAlreadyExists()
        
        _BRAZIL_TIMEZONE_ = pytz.timezone("America/Sao_Paulo")
        
        plan_db = Plan(
            name = plan_data.name,
            description = plan_data.description,
            price = plan_data.price,
            created_at = datetime.now(_BRAZIL_TIMEZONE_),
            updated_at = datetime.now(_BRAZIL_TIMEZONE_)
        )

        new_plan = await self.__plan_repository.create(plan_db)

        return new_plan
    

    async def list_plans(
        self,
        limit: int,
        offset: int,
        search: str | None
    ) -> List[Plan]:
        
        plans = await self.__plan_repository.get_all_plans(
            limit, offset, search
        )

        return plans
    
    async def get_by_id(self, plan_id: int):

        plan = await self.__plan_repository.get_by_id(plan_id)

        if not plan:

            raise PlanNotFound()
        
        return plan

    async def delete_plan(self, company_repository: CompanyRepository,  plan_id: int) -> None:

        plan = await self.__plan_repository.get_by_id(plan_id)

        if not plan:

            raise PlanNotFound()
        
        have_companys = await company_repository.verify_if_plan_id(plan_id)

        if have_companys:

            raise PlanHaveCompanys()
        
        await self.__plan_repository.delete(plan_id)

