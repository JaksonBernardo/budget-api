import pytest
from unittest.mock import AsyncMock, MagicMock
from decimal import Decimal
from api.services.prices import PriceService
from api.schemas.prices import PriceSchema
from api.models.prices import Price
from api.exceptions import (
    CompanyNotFound
)
from api.exceptions.prices import (
    PriceNotFound
)

@pytest.fixture
def mock_price_repository():
    return MagicMock()

@pytest.fixture
def mock_company_repository():
    return MagicMock()

@pytest.fixture
def price_service(mock_price_repository, mock_company_repository):
    return PriceService(mock_price_repository, mock_company_repository)

@pytest.fixture
def sample_price_schema():
    return PriceSchema(
        name="Standard Price",
        fixed_expenses=Decimal("10.00"),
        impost=Decimal("15.00"),
        commission=Decimal("5.00"),
        others_rates=Decimal("2.00"),
        profit_margin=Decimal("20.00"),
        markup=Decimal("1.80"),
        company_id=1
    )

class TestPriceService:
    @pytest.mark.asyncio
    async def test_create_price_success(self, price_service, mock_company_repository, mock_price_repository, sample_price_schema):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_price = MagicMock(spec=Price)
        mock_price_repository.save = AsyncMock(return_value=mock_price)

        result = await price_service.create(sample_price_schema)

        assert result == mock_price
        mock_company_repository.get_by_id.assert_called_once_with(1)
        mock_price_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_price_company_not_found(self, price_service, mock_company_repository, sample_price_schema):
        mock_company_repository.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(CompanyNotFound):
            await price_service.create(sample_price_schema)

    @pytest.mark.asyncio
    async def test_list_prices_success(self, price_service, mock_company_repository, mock_price_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_price_repository.get_by_company_id = AsyncMock(return_value=[])

        result = await price_service.list(company_id=1)

        assert result == []
        mock_price_repository.get_by_company_id.assert_called_once_with(1, 0, 20, None)

    @pytest.mark.asyncio
    async def test_get_price_success(self, price_service, mock_company_repository, mock_price_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_price = MagicMock(spec=Price)
        mock_price_repository.get_by_id = AsyncMock(return_value=mock_price)

        result = await price_service.get(1, 1)

        assert result == mock_price

    @pytest.mark.asyncio
    async def test_delete_price_success(self, price_service, mock_company_repository, mock_price_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_price_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_price_repository.delete_by_id = AsyncMock()

        await price_service.delete(1, 1)

        mock_price_repository.delete_by_id.assert_called_once_with(1, 1)

    @pytest.mark.asyncio
    async def test_update_price_success(self, price_service, mock_company_repository, mock_price_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        existing_price = MagicMock(spec=Price)
        existing_price.company_id = 1
        mock_price_repository.get_by_id = AsyncMock(return_value=existing_price)
        mock_price_repository.update = AsyncMock(return_value=existing_price)

        update_data = {
            "name": "Updated Price",
            "fixed_expenses": Decimal("12.00")
        }
        result = await price_service.update(1, 1, update_data)

        assert result == existing_price
        assert existing_price.name == "Updated Price"
        assert existing_price.fixed_expenses == Decimal("12.00")
        mock_price_repository.update.assert_called_once()
