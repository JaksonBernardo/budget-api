import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
import pytz
from api.services.employees import EmployeeService
from api.schemas.employees import EmployeeSchema
from api.models.employees import Employee
from api.exceptions import (
    CompanyNotFound,
    EmployeeNotFound,
    EmployeeInvalidData
)

@pytest.fixture
def mock_employee_repository():
    return MagicMock()

@pytest.fixture
def mock_company_repository():
    return MagicMock()

@pytest.fixture
def employee_service(mock_employee_repository, mock_company_repository):
    return EmployeeService(mock_employee_repository, mock_company_repository)

@pytest.fixture
def sample_employee_schema():
    return EmployeeSchema(
        name="John Doe",
        function_name="Developer",
        money=5000.0,
        hours_per_month=160,
        food_assistance=500.0,
        transport_assistance=200.0,
        others_benefits=100.0,
        health_plan=300.0,
        cost_per_minute=0.5,
        user_id=1,
        company_id=1
    )

class TestEmployeeService:
    @pytest.mark.asyncio
    async def test_create_employee_success(self, employee_service, mock_company_repository, mock_employee_repository, sample_employee_schema):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_employee = MagicMock(spec=Employee)
        mock_employee_repository.save = AsyncMock(return_value=mock_employee)

        result = await employee_service.create(sample_employee_schema)

        assert result == mock_employee
        mock_company_repository.get_by_id.assert_called_once_with(1)
        mock_employee_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_employee_company_not_found(self, employee_service, mock_company_repository, sample_employee_schema):
        mock_company_repository.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(CompanyNotFound):
            await employee_service.create(sample_employee_schema)

    @pytest.mark.asyncio
    async def test_list_employees_success(self, employee_service, mock_company_repository, mock_employee_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_employee_repository.get_by_company_id = AsyncMock(return_value=[])

        result = await employee_service.list(company_id=1, offset=0, limit=20, search=None)

        assert result == []
        mock_employee_repository.get_by_company_id.assert_called_once_with(1, 0, 20, None)

    @pytest.mark.asyncio
    async def test_list_employees_with_search(self, employee_service, mock_company_repository, mock_employee_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_employee_repository.get_by_company_id = AsyncMock(return_value=[])

        await employee_service.list(company_id=1, offset=0, limit=20, search="John")

        mock_employee_repository.get_by_company_id.assert_called_once_with(1, 0, 20, "%John%")

    @pytest.mark.asyncio
    async def test_list_employees_company_not_found(self, employee_service, mock_company_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(CompanyNotFound):
            await employee_service.list(company_id=1, offset=0, limit=20, search=None)

    @pytest.mark.asyncio
    async def test_get_employee_success(self, employee_service, mock_company_repository, mock_employee_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_employee = MagicMock(spec=Employee)
        mock_employee_repository.get_by_id = AsyncMock(return_value=mock_employee)

        result = await employee_service.get(1, 1)

        assert result == mock_employee
        mock_employee_repository.get_by_id.assert_called_once_with(1, 1)

    @pytest.mark.asyncio
    async def test_get_employee_not_found(self, employee_service, mock_company_repository, mock_employee_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_employee_repository.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(EmployeeNotFound):
            await employee_service.get(1, 1)

    @pytest.mark.asyncio
    async def test_delete_employee_success(self, employee_service, mock_company_repository, mock_employee_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_employee_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_employee_repository.delete_by_id = AsyncMock()

        await employee_service.delete(1, 1)

        mock_employee_repository.delete_by_id.assert_called_once_with(1, 1)

    @pytest.mark.asyncio
    async def test_update_employee_success(self, employee_service, mock_company_repository, mock_employee_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        existing_employee = MagicMock(spec=Employee)
        mock_employee_repository.get_by_id = AsyncMock(return_value=existing_employee)
        mock_employee_repository.update = AsyncMock(return_value=existing_employee)

        update_data = {"company_id": 1, "name": "New Name"}
        result = await employee_service.update(1, update_data)

        assert result == existing_employee
        assert existing_employee.name == "New Name"
        mock_employee_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_employee_no_company_id(self, employee_service):
        with pytest.raises(EmployeeInvalidData):
            await employee_service.update(1, {"name": "New Name"})

    @pytest.mark.asyncio
    async def test_update_employee_empty_name(self, employee_service, mock_company_repository, mock_employee_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_employee_repository.get_by_id = AsyncMock(return_value=MagicMock())

        with pytest.raises(EmployeeInvalidData):
            await employee_service.update(1, {"company_id": 1, "name": ""})
