from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import StatusBudget
from api.repositories import (
    StatusBudgetRepository,
    CompanyRepository
)
from api.schemas import (
    StatusBudgetSchema,
    StatusBudgetUpdateSchema
)
from api.exceptions import (
    CompanyNotFound,
    StatusBudgetNotFound,
    StatusBudgetIsSaleAlreadyExists
)
from datetime import datetime
import pytz

class StatusBudgetService:

    def __init__(
        self,
        company_repository: CompanyRepository,
        status_budget_repository: StatusBudgetRepository,
        db: AsyncSession
    ) -> None:
        
        self.__company_repository = company_repository
        self.__status_budget_repository = status_budget_repository
        self.__db = db

    async def create(self, status_data: StatusBudgetSchema) -> StatusBudget:

        try:
            company = await self.__company_repository.get_by_id(status_data.company_id)
            if not company: raise CompanyNotFound()
            
            if status_data.is_sale:
                existing_is_sale = await self.__status_budget_repository.get_is_sale_by_company_id(status_data.company_id)
                if existing_is_sale: raise StatusBudgetIsSaleAlreadyExists()

            _BRAZIL_TIMEZONE_ = pytz.timezone("America/Sao_Paulo")
            
            status_entity = StatusBudget(
                name = status_data.name,
                color = status_data.color,
                is_sale = status_data.is_sale,
                company_id = status_data.company_id,
                created_at = datetime.now(_BRAZIL_TIMEZONE_),
                updated_at = datetime.now(_BRAZIL_TIMEZONE_)
            )
            
            status = await self.__status_budget_repository.save(status_entity)
            await self.__db.commit()
            
            return status

        except Exception as ex:
            await self.__db.rollback()
            raise ex

    async def list(self, company_id: int, offset: int, limit: int, search: Optional[str] = None) -> List[StatusBudget]:
        
        company = await self.__company_repository.get_by_id(company_id)
        if not company: raise CompanyNotFound()
        
        return await self.__status_budget_repository.get_by_company_id(company_id, offset, limit, search)

    async def get(self, company_id: int, status_id: int) -> StatusBudget:
        
        company = await self.__company_repository.get_by_id(company_id)
        if not company: raise CompanyNotFound()
        
        status = await self.__status_budget_repository.get_by_id(company_id, status_id)
        if not status: raise StatusBudgetNotFound()
        
        return status

    async def update(self, company_id: int, status_id: int, status_data: StatusBudgetUpdateSchema) -> StatusBudget:
        
        try:
            await self.get(company_id, status_id)
            
            if status_data.is_sale:
                existing_is_sale = await self.__status_budget_repository.get_is_sale_by_company_id(company_id, exclude_id=status_id)
                if existing_is_sale: raise StatusBudgetIsSaleAlreadyExists()
            
            update_data = status_data.model_dump(exclude_unset=True)
            
            _BRAZIL_TIMEZONE_ = pytz.timezone("America/Sao_Paulo")
            update_data["updated_at"] = datetime.now(_BRAZIL_TIMEZONE_)
            
            updated_status = await self.__status_budget_repository.update(company_id, status_id, update_data)
            await self.__db.commit()
            
            return updated_status
            
        except Exception as ex:
            await self.__db.rollback()
            raise ex

    async def delete(self, company_id: int, status_id: int) -> None:
        
        try:
            await self.get(company_id, status_id)
            
            await self.__status_budget_repository.delete(company_id, status_id)
            await self.__db.commit()
            
        except Exception as ex:
            await self.__db.rollback()
            raise ex
