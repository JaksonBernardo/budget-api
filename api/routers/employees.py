from typing import Optional
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import (
    CompanyNotFound,
    EmployeeNotFound,
    EmployeeInvalidData,
    EmployeeAccessDenied
)
from api.exceptions.map_exceptions import map_exception
from api.repositories import EmployeeRepository, CompanyRepository
from api.core.database import get_session
from api.schemas import (
    EmployeeSchema,
    EmployeePublicSchema,
    ListEmployeePublicSchema,
    EmployeeUpdateSchema
)
from api.services.employees import EmployeeService
from api.security.dependencies import CurrentUser

employee_router = APIRouter(
    prefix = "/api/v1/employees",
    tags = ["Employees"]
)

def get_employee_repository(db: AsyncSession = Depends(get_session)) -> EmployeeRepository:
    return EmployeeRepository(db)

def get_company_repository(db: AsyncSession = Depends(get_session)) -> CompanyRepository:
    return CompanyRepository(db)

def get_employee_service(
    employee_repository: EmployeeRepository = Depends(get_employee_repository),
    company_repository: CompanyRepository = Depends(get_company_repository)
) -> EmployeeService:
    return EmployeeService(employee_repository, company_repository)


@employee_router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Criando um colaborador",
    response_model = EmployeePublicSchema
)
async def create_employee(
    employee_data: EmployeeSchema,
    service: EmployeeService = Depends(get_employee_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        new_employee = await service.create(employee_data)
        return new_employee

    except (CompanyNotFound, EmployeeInvalidData) as e:
        raise map_exception(e)


@employee_router.get(
    path = "/{company_id}",
    status_code = status.HTTP_200_OK,
    summary = "Listando todos os colaboradores",
    response_model = ListEmployeePublicSchema
)
async def list_employees(
    company_id: int,
    service: EmployeeService = Depends(get_employee_service),
    current_user: CurrentUser = CurrentUser,
    offset: int = Query(0, ge = 0, description = "Registros a serem pulados"),
    limit: int = Query(20, ge = 1, description = "Qtd máxima de registros apresentados"),
    search: Optional[str] = Query(None, description = "Pesquisar pelo nome de algum colaborador")
):
    try:
        employees = await service.list(company_id, offset, limit, search)
        return {
            "employees": employees
        }

    except CompanyNotFound as e:
        raise map_exception(e)


@employee_router.get(
    path = "/{company_id}/{employee_id}",
    status_code = status.HTTP_200_OK,
    summary = "Selecionando um colaborador específico",
    response_model = EmployeePublicSchema
)
async def get_employee(
    company_id: int,
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        employee = await service.get(company_id, employee_id)
        return employee

    except (CompanyNotFound, EmployeeNotFound) as e:
        raise map_exception(e)


@employee_router.delete(
    path = "/{company_id}/{employee_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Deletando um colaborador específico"
)
async def delete_employee(
    company_id: int,
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        await service.delete(company_id, employee_id)

    except (CompanyNotFound, EmployeeNotFound) as e:
        raise map_exception(e)


@employee_router.put(
    path = "/{employee_id}",
    status_code = status.HTTP_200_OK,
    summary = "Atualizando um colaborador",
    response_model = EmployeePublicSchema
)
async def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdateSchema,
    service: EmployeeService = Depends(get_employee_service),
    current_user: CurrentUser = CurrentUser,
):
    try:
        employee_info = employee_data.model_dump(exclude_unset = True)
        employee = await service.update(employee_id, employee_info)
        return employee

    except (CompanyNotFound, EmployeeNotFound, EmployeeAccessDenied, EmployeeInvalidData) as e:
        raise map_exception(e)
