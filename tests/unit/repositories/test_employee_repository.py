import pytest
from unittest.mock import AsyncMock, MagicMock
from api.repositories.employees import EmployeeRepository
from api.models.employees import Employee

class TestEmployeeRepository:
    @pytest.mark.asyncio
    async def test_save_employee_success(self, mock_db_session):
        mock_employee = MagicMock(spec=Employee)
        repository = EmployeeRepository(mock_db_session)
        
        result = await repository.save(mock_employee)
        
        mock_db_session.add.assert_called_once_with(mock_employee)
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_employee)
        assert result == mock_employee

    @pytest.mark.asyncio
    async def test_save_employee_rollback_on_error(self, mock_db_session):
        mock_employee = MagicMock(spec=Employee)
        mock_db_session.commit.side_effect = Exception("DB Error")
        repository = EmployeeRepository(mock_db_session)
        
        with pytest.raises(Exception):
            await repository.save(mock_employee)
        
        mock_db_session.rollback.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_company_id_success(self, mock_db_session):
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = EmployeeRepository(mock_db_session)
        
        result = await repository.get_by_company_id(1, 0, 20, None)
        
        assert result == []
        mock_db_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, mock_db_session):
        mock_employee = MagicMock(spec=Employee)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_employee
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = EmployeeRepository(mock_db_session)
        
        result = await repository.get_by_id(1, 1)
        
        assert result == mock_employee
        mock_db_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, mock_db_session):
        mock_db_session.execute = AsyncMock()
        repository = EmployeeRepository(mock_db_session)
        
        await repository.delete_by_id(1, 1)
        
        mock_db_session.execute.assert_called_once()
        mock_db_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_success(self, mock_db_session):
        mock_employee = MagicMock(spec=Employee)
        repository = EmployeeRepository(mock_db_session)
        
        result = await repository.update(mock_employee)
        
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_employee)
        assert result == mock_employee
