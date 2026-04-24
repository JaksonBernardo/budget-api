import pytest
from unittest.mock import AsyncMock, MagicMock
from api.repositories.plans import PlanRepository
from api.models.plans import Plan

class TestPlanRepository:
    @pytest.mark.asyncio
    async def test_create_plan_success(self, mock_db_session):
        mock_plan = MagicMock(spec=Plan)
        repository = PlanRepository(mock_db_session)
        
        result = await repository.create(mock_plan)
        
        mock_db_session.add.assert_called_once_with(mock_plan)
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_plan)
        assert result == mock_plan

    @pytest.mark.asyncio
    async def test_verify_exists_by_name(self, mock_db_session):
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = MagicMock()
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = PlanRepository(mock_db_session)
        
        result = await repository.verify_exists_by_name("Test Plan")
        
        assert result is not None

    @pytest.mark.asyncio
    async def test_get_all_plans(self, mock_db_session):
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = PlanRepository(mock_db_session)
        
        result = await repository.get_all_plans(limit=10, offset=0, search="test")
        
        assert result == []

    @pytest.mark.asyncio
    async def test_get_by_id(self, mock_db_session):
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = MagicMock()
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = PlanRepository(mock_db_session)
        
        result = await repository.get_by_id(1)
        
        assert result is not None

    @pytest.mark.asyncio
    async def test_delete_success(self, mock_db_session):
        mock_db_session.execute = AsyncMock()
        repository = PlanRepository(mock_db_session)
        
        await repository.delete(1)
        
        mock_db_session.execute.assert_called_once()
        mock_db_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_success(self, mock_db_session):
        mock_plan = MagicMock(spec=Plan)
        repository = PlanRepository(mock_db_session)
        
        result = await repository.update(mock_plan)
        
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_plan)
        assert result == mock_plan
