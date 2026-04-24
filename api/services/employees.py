import pytz
from typing import Dict, List, Optional
from datetime import datetime
from api.models.employees import Employee
from api.repositories import EmployeeRepository, CompanyRepository
from api.schemas.employees import EmployeeSchema
from api.exceptions import (
    CompanyNotFound,
    EmployeeNotFound,
    EmployeeInvalidData,
    EmployeeAccessDenied
)

class EmployeeService:
    def __init__(
        self,
        employee_repository: EmployeeRepository,
        company_repository: CompanyRepository
    ):
        self._employee_repository = employee_repository
        self._company_repository = company_repository

    async def create(self, employee_data: EmployeeSchema) -> Employee:
        company = await self._company_repository.get_by_id(employee_data.company_id)
        if not company:
            raise CompanyNotFound()

        employee = Employee(
            name=employee_data.name,
            function_name=employee_data.function_name,
            money=employee_data.money,
            hours_per_month=employee_data.hours_per_month,
            food_assistance=employee_data.food_assistance,
            transport_assistance=employee_data.transport_assistance,
            others_benefits=employee_data.others_benefits,
            health_plan=employee_data.health_plan,
            cost_per_minute=employee_data.cost_per_minute,
            user_id=employee_data.user_id,
            company_id=employee_data.company_id
        )

        return await self._employee_repository.save(employee)

    async def list(
        self,
        company_id: int,
        offset: int,
        limit: int,
        search: Optional[str]
    ) -> List[Employee]:
        company = await self._company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFound()

        if search:
            search = f"%{search}%"

        return await self._employee_repository.get_by_company_id(
            company_id,
            offset,
            limit,
            search
        )

    async def get(self, company_id: int, employee_id: int) -> Employee:
        company = await self._company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFound()

        employee = await self._employee_repository.get_by_id(company_id, employee_id)
        if not employee:
            raise EmployeeNotFound()

        return employee

    async def delete(self, company_id: int, employee_id: int) -> None:
        company = await self._company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFound()

        employee = await self._employee_repository.get_by_id(company_id, employee_id)
        if not employee:
            raise EmployeeNotFound()

        await self._employee_repository.delete_by_id(company_id, employee_id)

    async def update(self, employee_id: int, employee_data: Dict) -> Employee:
        if "company_id" not in employee_data:
             raise EmployeeInvalidData("company_id é obrigatório para atualização")

        company = await self._company_repository.get_by_id(employee_data["company_id"])
        if not company:
            raise CompanyNotFound()

        employee = await self._employee_repository.get_by_id(
            employee_data["company_id"],
            employee_id
        )

        if not employee:
            raise EmployeeNotFound()

        if "name" in employee_data and not employee_data["name"]:
            raise EmployeeInvalidData("Nome não pode ser vazio")

        _BRAZIL_TIMEZONE_ = pytz.timezone("America/Sao_Paulo")
        
        for key, value in employee_data.items():
            if hasattr(employee, key) and key not in ["id", "created_at", "updated_at"]:
                setattr(employee, key, value)
        
        employee.updated_at = datetime.now(_BRAZIL_TIMEZONE_)

        return await self._employee_repository.update(employee)
