import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch, MagicMock
from decimal import Decimal
from datetime import date
from api.models.budgets import TypeDiscount

@pytest.fixture
async def test_client():
    from api.app import app
    from api.security.dependencies import get_current_user
    
    mock_user = MagicMock()
    mock_user.id = 1
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()

class TestBudgetEndpoints:
    @pytest.mark.asyncio
    async def test_create_budget_success(self, test_client: AsyncClient):
        with patch("api.services.budgets.BudgetService.create", new_callable=AsyncMock) as mock_create:
            mock_budget = MagicMock()
            mock_budget.id = 1
            mock_budget.client_id = 1
            mock_budget.user_id = 1
            mock_budget.validity_date = date(2026, 6, 1)
            mock_budget.date_acceptance = date(2026, 5, 10)
            mock_budget.date_starter_services = date(2026, 5, 15)
            mock_budget.status_id = 1
            mock_budget.payment_condition = 1
            mock_budget.type_discount = TypeDiscount.FIXED
            mock_budget.value_discount = Decimal("10.00")
            mock_budget.total_value = Decimal("90.00") # Mocked total value
            mock_budget.company_id = 1
            mock_budget.created_at = date(2026, 5, 9)
            mock_budget.updated_at = date(2026, 5, 9)
            mock_budget.services = []
            
            mock_create.return_value = mock_budget
            
            payload = {
                "client_id": 1,
                "user_id": 1,
                "validity_date": "2026-06-01",
                "date_acceptance": "2026-05-10",
                "date_starter_services": "2026-05-15",
                "status_id": 1,
                "payment_condition": 1,
                "type_discount": "FIXED",
                "value_discount": "10.00",
                "company_id": 1,
                "services": [
                    {
                        "service_id": 1,
                        "price_id": 10,
                        "qtd": 2,
                        "service_value": "50.00"
                    }
                ]
            }
            
            response = await test_client.post("/api/v1/budgets/", json=payload)
            
            assert response.status_code == 201
            data = response.json()
            assert data["id"] == 1
            assert data["total_value"] == "90.00"

    @pytest.mark.asyncio
    async def test_create_budget_invalid_price_id(self, test_client: AsyncClient):
        with patch("api.services.budgets.BudgetService.create", new_callable=AsyncMock) as mock_create:
            from api.exceptions import ServicePriceNotFound
            mock_create.side_effect = ServicePriceNotFound()
            
            payload = {
                "client_id": 1,
                "user_id": 1,
                "validity_date": "2026-06-01",
                "date_acceptance": "2026-05-10",
                "date_starter_services": "2026-05-15",
                "status_id": 1,
                "payment_condition": 1,
                "type_discount": "FIXED",
                "value_discount": "10.00",
                "company_id": 1,
                "services": [
                    {
                        "service_id": 1,
                        "price_id": 999, # Invalid
                        "qtd": 2,
                        "service_value": "50.00"
                    }
                ]
            }
            
            response = await test_client.post("/api/v1/budgets/", json=payload)
            
            assert response.status_code == 404
            assert response.json()["detail"] == "O preço informado não pertence a este serviço"
