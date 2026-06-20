import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch, MagicMock
from decimal import Decimal
from datetime import date, datetime
from api.models.projects import ProjectOrigin

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

class TestProjectEndpoints:
    @pytest.mark.asyncio
    async def test_create_project_success(self, test_client: AsyncClient):
        with patch("api.services.projects.ProjectService.create", new_callable=AsyncMock) as mock_create:
            mock_project = MagicMock()
            mock_project.id = 1
            mock_project.budget_id = 1
            mock_project.client_id = 1
            mock_project.code = "PRJ-001"
            mock_project.origin = ProjectOrigin.MANUAL
            mock_project.campaign = 1
            mock_project.company_id = 1
            mock_project.status_id = 1
            mock_project.start_date = date(2026, 6, 1)
            mock_project.estimated_end_date = date(2026, 6, 30)
            mock_project.end_date = None
            mock_project.notes = "Test notes"
            mock_project.created_at = datetime(2026, 6, 6, 12, 0, 0)
            mock_project.updated_at = datetime(2026, 6, 6, 12, 0, 0)

            mock_service = MagicMock()
            mock_service.id = 1
            mock_service.service_id = 1
            mock_service.service_name = "Test Service"
            mock_service.service_qtd = 2
            mock_service.service_value = Decimal("50.00")
            mock_service.service_total_value = Decimal("100.00")
            mock_service.start_date = None
            mock_service.delivery_date = None

            mock_material = MagicMock()
            mock_material.id = 1
            mock_material.project_service_id = 1
            mock_material.material_id = 1
            mock_material.material_name = "Test Material"
            mock_material.quantity = Decimal("10.00")
            mock_material.unit_cost = Decimal("5.00")
            mock_material.total_cost = Decimal("50.00")

            mock_service.materials = [mock_material]
            mock_project.services = [mock_service]
            
            mock_create.return_value = mock_project
            
            payload = {
                "budget_id": 1,
                "client_id": 1,
                "code": "PRJ-001",
                "origin": "MANUAL",
                "campaign": 1,
                "company_id": 1,
                "status_id": 1,
                "start_date": "2026-06-01",
                "estimated_end_date": "2026-06-30",
                "notes": "Test notes",
                "services": [
                    {
                        "service_id": 1,
                        "service_name": "Test Service",
                        "service_qtd": 2,
                        "service_value": "50.00"
                    }
                ]
            }
            
            response = await test_client.post("/api/v1/projects/", json=payload)
            
            assert response.status_code == 201
            data = response.json()
            assert data["id"] == 1
            assert data["code"] == "PRJ-001"
            assert data["services"][0]["start_date"] is None
            assert data["services"][0]["delivery_date"] is None
            assert len(data["services"][0]["materials"]) == 1
            assert data["services"][0]["materials"][0]["material_name"] == "Test Material"
            assert data["services"][0]["materials"][0]["total_cost"] == "50.00"

    @pytest.mark.asyncio
    async def test_create_project_without_budget_id_success(self, test_client: AsyncClient):
        with patch("api.services.projects.ProjectService.create", new_callable=AsyncMock) as mock_create:
            mock_project = MagicMock()
            mock_project.id = 2
            mock_project.budget_id = None
            mock_project.client_id = 1
            mock_project.code = "PRJ-002"
            mock_project.origin = ProjectOrigin.MANUAL
            mock_project.campaign = 1
            mock_project.company_id = 1
            mock_project.status_id = 1
            mock_project.start_date = date(2026, 6, 1)
            mock_project.estimated_end_date = None
            mock_project.end_date = None
            mock_project.notes = None
            mock_project.created_at = datetime(2026, 6, 6, 12, 0, 0)
            mock_project.updated_at = datetime(2026, 6, 6, 12, 0, 0)
            mock_project.services = []
            
            mock_create.return_value = mock_project
            
            payload = {
                "client_id": 1,
                "code": "PRJ-002",
                "origin": "MANUAL",
                "company_id": 1,
                "status_id": 1,
                "start_date": "2026-06-01",
                "services": []
            }
            
            response = await test_client.post("/api/v1/projects/", json=payload)
            
            assert response.status_code == 201
            data = response.json()
            assert data["id"] == 2
            assert data["budget_id"] is None
            assert data["code"] == "PRJ-002"

    @pytest.mark.asyncio
    async def test_create_project_company_not_found(self, test_client: AsyncClient):
        with patch("api.services.projects.ProjectService.create", new_callable=AsyncMock) as mock_create:
            from api.exceptions import CompanyNotFound
            mock_create.side_effect = CompanyNotFound()
            
            payload = {
                "budget_id": 1,
                "client_id": 1,
                "code": "PRJ-001",
                "origin": "MANUAL",
                "company_id": 999,
                "status_id": 1,
                "start_date": "2026-06-01",
                "services": []
            }
            
            response = await test_client.post("/api/v1/projects/", json=payload)
            
            assert response.status_code == 404
            assert response.json()["detail"] == "Company não encontrada"

    @pytest.mark.asyncio
    async def test_update_service_delivery_success(self, test_client: AsyncClient):
        with patch("api.services.projects.ProjectService.update_service_delivery", new_callable=AsyncMock) as mock_update:
            mock_service = MagicMock()
            mock_service.id = 1
            mock_service.service_id = 10
            mock_service.service_name = "Delivered Service"
            mock_service.service_qtd = 1
            mock_service.service_value = Decimal("100.00")
            mock_service.service_total_value = Decimal("100.00")
            mock_service.is_delivered = True
            mock_service.start_date = None
            mock_service.delivery_date = None
            
            mock_update.return_value = mock_service
            
            payload = {"is_delivered": True}
            
            response = await test_client.patch("/api/v1/projects/services/1/delivery", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 1
            assert data["is_delivered"] is True
            assert data["service_name"] == "Delivered Service"
