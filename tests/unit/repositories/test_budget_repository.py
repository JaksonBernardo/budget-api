import pytest
from unittest.mock import AsyncMock, MagicMock
from api.repositories.budgets import BudgetRepository, BudgetServiceRepository
from api.models.budgets import Budget, BudgetService

class TestBudgetRepository:
    @pytest.mark.asyncio
    async def test_save_budget_success(self, mock_db_session):
        mock_budget = MagicMock(spec=Budget)
        repository = BudgetRepository(mock_db_session)
        
        result = await repository.save(mock_budget)
        
        mock_db_session.add.assert_called_once_with(mock_budget)
        mock_db_session.flush.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_budget)
        assert result == mock_budget

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, mock_db_session):
        mock_budget = MagicMock(spec=Budget)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_budget
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = BudgetRepository(mock_db_session)
        
        result = await repository.get_by_id(company_id=1, budget_id=1)
        
        assert result == mock_budget

class TestBudgetServiceRepository:
    @pytest.mark.asyncio
    async def test_save_budget_services_success(self, mock_db_session):
        repository = BudgetServiceRepository(mock_db_session)
        list_budget_service = [{"budget_id": 1, "service_id": 1, "price_id": 10, "qtd": 2, "service_value": 50.0, "total_value": 100.0}]
        
        await repository.save(list_budget_service)
        
        mock_db_session.execute.assert_called_once()
        mock_db_session.flush.assert_called_once()
