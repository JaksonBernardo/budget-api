import pytest
from unittest.mock import AsyncMock, MagicMock
from decimal import Decimal
from datetime import date
from api.services.budgets import BudgetService
from api.schemas.budgets import BudgetSchema, BudgetServicesSchema
from api.models.budgets import TypeDiscount
from api.exceptions import (
    CompanyNotFound,
    ClientNotFound,
    UserNotFound,
    ServiceNotFound,
    ServicePriceNotFound
)

@pytest.fixture
def mock_company_repository():
    return MagicMock()

@pytest.fixture
def mock_precification_repository():
    return MagicMock()

@pytest.fixture
def mock_client_repository():
    return MagicMock()

@pytest.fixture
def mock_user_repository():
    return MagicMock()

@pytest.fixture
def mock_budget_repository():
    return MagicMock()

@pytest.fixture
def mock_budget_service_repository():
    return MagicMock()

@pytest.fixture
def mock_status_budget_repository():
    return MagicMock()

@pytest.fixture
def mock_payment_condition_repository():
    return MagicMock()

@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    return session

@pytest.fixture
def budget_service(
    mock_company_repository,
    mock_precification_repository,
    mock_client_repository,
    mock_user_repository,
    mock_budget_repository,
    mock_budget_service_repository,
    mock_status_budget_repository,
    mock_payment_condition_repository,
    mock_db_session
):
    return BudgetService(
        mock_company_repository,
        mock_precification_repository,
        mock_client_repository,
        mock_user_repository,
        mock_budget_repository,
        mock_budget_service_repository,
        mock_status_budget_repository,
        mock_payment_condition_repository,
        mock_db_session
    )

@pytest.fixture
def sample_budget_schema():
    return BudgetSchema(
        client_id=1,
        user_id=1,
        validity_date=date(2026, 6, 1),
        date_acceptance=date(2026, 5, 10),
        date_starter_services=date(2026, 5, 15),
        status_id=1,
        payment_condition=1,
        type_discount=TypeDiscount.FIXED,
        value_discount=Decimal("10.00"),
        company_id=1,
        services=[
            BudgetServicesSchema(
                service_id=1,
                price_id=10,
                qtd=2,
                service_value=Decimal("50.00"),
                total_value=Decimal("100.00")
            )
        ]
    )

class TestBudgetServiceCreate:
    @pytest.mark.asyncio
    async def test_create_budget_success(
        self, 
        budget_service, 
        mock_company_repository, 
        mock_client_repository, 
        mock_user_repository, 
        mock_precification_repository,
        mock_budget_repository,
        mock_budget_service_repository,
        mock_status_budget_repository,
        mock_payment_condition_repository,
        sample_budget_schema
    ):
        # Mocks
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_client_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_user_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_status_budget_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_payment_condition_repository.get_by_id = AsyncMock(return_value=MagicMock())
        
        # Mock service and its prices
        mock_service = MagicMock()
        mock_service.id = 1
        mock_price = MagicMock()
        mock_price.price_id = 10
        mock_service.prices = [mock_price]
        mock_precification_repository.get_by_ids = AsyncMock(return_value=[mock_service])
        
        # Mock budget save
        mock_budget = MagicMock()
        mock_budget.id = 100
        mock_budget.company_id = 1
        mock_budget_repository.save = AsyncMock(return_value=mock_budget)
        mock_budget_repository.get_by_id = AsyncMock(return_value=mock_budget)
        
        mock_budget_service_repository.save = AsyncMock()
        
        result = await budget_service.create(sample_budget_schema)
        
        assert result == mock_budget
        mock_budget_repository.save.assert_called_once()
        mock_budget_service_repository.save.assert_called_once()
        
        # Verify if price_id was passed correctly to budget_service_repository.save
        args, _ = mock_budget_service_repository.save.call_args
        assert args[0][0]["price_id"] == 10

    @pytest.mark.asyncio
    async def test_create_budget_invalid_price_id(
        self, 
        budget_service, 
        mock_company_repository, 
        mock_client_repository, 
        mock_user_repository, 
        mock_precification_repository,
        mock_status_budget_repository,
        mock_payment_condition_repository,
        sample_budget_schema
    ):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_client_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_user_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_status_budget_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_payment_condition_repository.get_by_id = AsyncMock(return_value=MagicMock())
        
        # Mock service with DIFFERENT price_id
        mock_service = MagicMock()
        mock_service.id = 1
        mock_price = MagicMock()
        mock_price.price_id = 99  # Different from 10 in schema
        mock_service.prices = [mock_price]
        mock_precification_repository.get_by_ids = AsyncMock(return_value=[mock_service])
        
        with pytest.raises(ServicePriceNotFound):
            await budget_service.create(sample_budget_schema)

    @pytest.mark.asyncio
    async def test_create_budget_service_not_found(
        self, 
        budget_service, 
        mock_company_repository, 
        mock_client_repository, 
        mock_user_repository, 
        mock_precification_repository,
        mock_status_budget_repository,
        mock_payment_condition_repository,
        sample_budget_schema
    ):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_client_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_user_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_status_budget_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_payment_condition_repository.get_by_id = AsyncMock(return_value=MagicMock())
        
        # Return empty list for services
        mock_precification_repository.get_by_ids = AsyncMock(return_value=[])
        
        with pytest.raises(ServiceNotFound):
            await budget_service.create(sample_budget_schema)

    @pytest.mark.asyncio
    async def test_create_budget_company_not_found(
        self, 
        budget_service, 
        mock_company_repository, 
        mock_client_repository,
        mock_user_repository,
        mock_status_budget_repository,
        mock_payment_condition_repository,
        sample_budget_schema
    ):
        mock_company_repository.get_by_id = AsyncMock(return_value=None)
        mock_client_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_user_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_status_budget_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_payment_condition_repository.get_by_id = AsyncMock(return_value=MagicMock())
        
        with pytest.raises(CompanyNotFound):
            await budget_service.create(sample_budget_schema)
