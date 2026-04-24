import pytest
from unittest.mock import AsyncMock, MagicMock
from api.services.plans import PlanService
from api.schemas.plans import PlanSchema
from api.models.plans import Plan
from api.exceptions.plans import (
    PlanNegativePrice,
    PlanNotFound,
    PlanAlreadyExists,
    PlanHaveCompanys
)

@pytest.fixture
def mock_plan_repository():
    return MagicMock()

@pytest.fixture
def plan_service(mock_plan_repository):
    return PlanService(mock_plan_repository)

@pytest.fixture
def sample_plan_schema():
    return PlanSchema(
        name="Premium Plan",
        description="Premium Plan Description",
        price=200.0
    )

class TestPlanService:
    @pytest.mark.asyncio
    async def test_create_plan_success(self, plan_service, mock_plan_repository, sample_plan_schema):
        mock_plan_repository.verify_exists_by_name = AsyncMock(return_value=None)
        mock_plan = MagicMock(spec=Plan)
        mock_plan_repository.create = AsyncMock(return_value=mock_plan)

        result = await plan_service.create(sample_plan_schema)

        assert result == mock_plan
        mock_plan_repository.verify_exists_by_name.assert_called_once_with("Premium Plan")
        mock_plan_repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_plan_already_exists(self, plan_service, mock_plan_repository, sample_plan_schema):
        mock_plan_repository.verify_exists_by_name = AsyncMock(return_value=MagicMock())

        with pytest.raises(PlanAlreadyExists):
            await plan_service.create(sample_plan_schema)

    @pytest.mark.asyncio
    async def test_create_plan_negative_price(self, plan_service, mock_plan_repository):
        mock_plan_repository.verify_exists_by_name = AsyncMock(return_value=None)
        schema = PlanSchema(name="Free", description="Free", price=-10.0)

        with pytest.raises(PlanNegativePrice):
            await plan_service.create(schema)

    @pytest.mark.asyncio
    async def test_list_plans_success(self, plan_service, mock_plan_repository):
        mock_plan_repository.get_all_plans = AsyncMock(return_value=[])

        result = await plan_service.list_plans(limit=10, offset=0, search=None)

        assert result == []

    @pytest.mark.asyncio
    async def test_delete_plan_success(self, plan_service, mock_plan_repository):
        mock_company_repository = MagicMock()
        mock_plan_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_company_repository.verify_if_plan_id = AsyncMock(return_value=False)
        mock_plan_repository.delete = AsyncMock()

        await plan_service.delete_plan(mock_company_repository, 1)

        mock_plan_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_plan_have_companys(self, plan_service, mock_plan_repository):
        mock_company_repository = MagicMock()
        mock_plan_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_company_repository.verify_if_plan_id = AsyncMock(return_value=True)

        with pytest.raises(PlanHaveCompanys):
            await plan_service.delete_plan(mock_company_repository, 1)

    @pytest.mark.asyncio
    async def test_update_plan_success(self, plan_service, mock_plan_repository):
        existing_plan = MagicMock(spec=Plan)
        existing_plan.name = "Old Name"
        existing_plan.description = "Old Desc"
        existing_plan.price = 100.0
        mock_plan_repository.get_by_id = AsyncMock(return_value=existing_plan)
        mock_plan_repository.update = AsyncMock(return_value=existing_plan)

        update_data = {"name": "New Name", "price": 150.0}
        result = await plan_service.update_plan(1, update_data)

        assert result.name == "New Name"
        assert result.price == 150.0
        mock_plan_repository.update.assert_called_once()
