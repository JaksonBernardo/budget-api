"""Testes de integração para endpoints de empresas"""
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

@pytest.fixture
async def test_client():
    """Cria um cliente de teste usando ASGITransport"""
    from api.app import app
    from api.security.dependencies import get_current_user
    
    # Mock do usuário atual
    mock_user = MagicMock()
    mock_user.id = 1
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()

@pytest.fixture
def sample_company_public_obj():
    class MockCompany:
        def __init__(self):
            self.id = 1
            self.customer_id = "cus_123"
            self.photo = "photo.png"
            self.email = "test@company.com"
            self.name = "Test Company"
            self.address = "Address"
            self.number = 100
            self.state = "SP"
            self.cep = "12345-678"
            self.city = "Sao Paulo"
            self.cnpj = "12345678000199"
            self.phone = "11999999999"
            self.whatsapp = "11999999999"
            self.website = "www.test.com"
            self.is_blocked = False
            self.plan_id = 1
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
    return MockCompany()

class TestCompanyEndpoints:
    @pytest.mark.asyncio
    async def test_create_company_success(self, test_client: AsyncClient, sample_company_public_obj):
        with patch("api.services.companys.CompanyService.create", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = sample_company_public_obj
            
            response = await test_client.post("/api/v1/companies/", json={
                "name": "Test Company",
                "cnpj": "12345678000199",
                "email": "test@company.com",
                "plan_id": 1,
                "phone": "11999999999"
            })
            
            assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_list_companies_success(self, test_client: AsyncClient, sample_company_public_obj):
        with patch("api.services.companys.CompanyService.list", new_callable=AsyncMock) as mock_list:
            mock_list.return_value = [sample_company_public_obj]
            
            response = await test_client.get("/api/v1/companies/")
            
            assert response.status_code == 200
            assert "companys" in response.json()

    @pytest.mark.asyncio
    async def test_get_company_success(self, test_client: AsyncClient, sample_company_public_obj):
        with patch("api.services.companys.CompanyService.get_by_id", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = sample_company_public_obj
            
            response = await test_client.get("/api/v1/companies/1")
            
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_company_not_found(self, test_client: AsyncClient):
        with patch("api.services.companys.CompanyService.get_by_id", new_callable=AsyncMock) as mock_get:
            from api.exceptions.companys import CompanyNotFound
            mock_get.side_effect = CompanyNotFound()
            
            response = await test_client.get("/api/v1/companies/999")
            
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_company_success(self, test_client: AsyncClient):
        with patch("api.services.companys.CompanyService.delete_company", new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = None
            
            response = await test_client.delete("/api/v1/companies/1")
            
            assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_update_company_success(self, test_client: AsyncClient, sample_company_public_obj):
        with patch("api.services.companys.CompanyService.update_company", new_callable=AsyncMock) as mock_update:
            mock_update.return_value = sample_company_public_obj
            
            response = await test_client.put("/api/v1/companies/1", json={"name": "Updated Name"})
            
            assert response.status_code == 200
