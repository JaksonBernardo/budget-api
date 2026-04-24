import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from api.services.companys import CompanyService
from api.schemas.companys import CompanySchema
from api.models.companys import Company
from api.models.plans import Plan
from api.exceptions.companys import CompanyNotFound, NameAlreadyExists, CnpjAlreadyExists
from api.exceptions.plans import PlanNotFound

@pytest.fixture
def mock_company_repository():
    return MagicMock()

@pytest.fixture
def mock_plan_repository():
    return MagicMock()

@pytest.fixture
def mock_subscription_repository():
    return MagicMock()

@pytest.fixture
def company_service(mock_company_repository, mock_plan_repository, mock_subscription_repository):
    return CompanyService(mock_company_repository, mock_plan_repository, mock_subscription_repository)

@pytest.fixture
def sample_company_schema():
    return CompanySchema(
        name="Test Company",
        cnpj="12345678000199",
        email="test@company.com",
        plan_id=1,
        address="Test Address",
        number=100,
        state="SP",
        cep="12345-678",
        city="Sao Paulo",
        phone="11999999999",
        whatsapp="11999999999",
        website="www.test.com",
        is_blocked=False,
        photo=None
    )

@pytest.fixture
def sample_plan():
    plan = MagicMock(spec=Plan)
    plan.id = 1
    plan.name = "Basic Plan"
    plan.price = 100.0
    plan.description = "Basic description"
    return plan

class TestCompanyServiceCreate:
    @pytest.mark.asyncio
    async def test_create_company_success(self, company_service, mock_company_repository, mock_plan_repository, mock_subscription_repository, sample_company_schema, sample_plan):
        # Setup mocks
        mock_plan_repository.get_by_id = AsyncMock(return_value=sample_plan)
        mock_company_repository.get_by_name = AsyncMock(return_value=None)
        mock_company_repository.get_by_document = AsyncMock(return_value=None)
        
        mock_company = MagicMock(spec=Company)
        mock_company.id = 1
        mock_company_repository.create = AsyncMock(return_value=mock_company)
        mock_subscription_repository.create = AsyncMock(return_value=MagicMock())

        mock_asaas_customers = MagicMock()
        mock_asaas_customers_instance = MagicMock()
        mock_asaas_customers.return_value = mock_asaas_customers_instance
        mock_asaas_customers_instance.post_customer.return_value = {"id": "cus_123"}

        mock_asaas_subscriptions = MagicMock()
        mock_asaas_subscriptions_instance = MagicMock()
        mock_asaas_subscriptions.return_value = mock_asaas_subscriptions_instance
        mock_asaas_subscriptions_instance.post_subscription.return_value = {"id": "sub_123", "status": "ACTIVE", "billingType": "BOLETO", "cycle": "MONTHLY"}

        # Execute
        result = await company_service.create(sample_company_schema, mock_asaas_customers, mock_asaas_subscriptions)

        # Assert
        assert result.id == 1
        mock_plan_repository.get_by_id.assert_called_once_with(1)
        mock_company_repository.get_by_name.assert_called_once_with("Test Company")
        mock_company_repository.get_by_document.assert_called_once_with("12345678000199")
        mock_company_repository.create.assert_called_once()
        mock_subscription_repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_company_plan_not_found(self, company_service, mock_plan_repository, sample_company_schema):
        mock_plan_repository.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(PlanNotFound):
            await company_service.create(sample_company_schema, MagicMock(), MagicMock())

    @pytest.mark.asyncio
    async def test_create_company_name_already_exists(self, company_service, mock_company_repository, mock_plan_repository, sample_company_schema, sample_plan):
        mock_plan_repository.get_by_id = AsyncMock(return_value=sample_plan)
        mock_company_repository.get_by_name = AsyncMock(return_value=MagicMock())

        with pytest.raises(NameAlreadyExists):
            await company_service.create(sample_company_schema, MagicMock(), MagicMock())

    @pytest.mark.asyncio
    async def test_create_company_cnpj_already_exists(self, company_service, mock_company_repository, mock_plan_repository, sample_company_schema, sample_plan):
        mock_plan_repository.get_by_id = AsyncMock(return_value=sample_plan)
        mock_company_repository.get_by_name = AsyncMock(return_value=None)
        mock_company_repository.get_by_document = AsyncMock(return_value=MagicMock())

        with pytest.raises(CnpjAlreadyExists):
            await company_service.create(sample_company_schema, MagicMock(), MagicMock())

class TestCompanyServiceList:
    @pytest.mark.asyncio
    async def test_list_companys_success(self, company_service, mock_company_repository):
        mock_company_repository.get_all = AsyncMock(return_value=[])
        
        result = await company_service.list(limit=10, offset=0, search=None)
        
        assert result == []
        mock_company_repository.get_all.assert_called_once_with(10, 0, None)

class TestCompanyServiceGet:
    @pytest.mark.asyncio
    async def test_get_company_by_id_success(self, company_service, mock_company_repository):
        mock_company = MagicMock(spec=Company)
        mock_company_repository.get_by_id = AsyncMock(return_value=mock_company)
        
        result = await company_service.get_by_id(1)
        
        assert result == mock_company
        mock_company_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_company_by_id_not_found(self, company_service, mock_company_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=None)
        
        with pytest.raises(CompanyNotFound):
            await company_service.get_by_id(999)

class TestCompanyServiceUpdate:
    @pytest.mark.asyncio
    async def test_update_company_success(self, company_service, mock_company_repository, mock_plan_repository):
        # Setup
        company_id = 1
        existing_company = MagicMock(spec=Company)
        existing_company.id = company_id
        existing_company.name = "Old Name"
        existing_company.cnpj = "12345678000199"
        existing_company.plan_id = 1
        existing_company.customer_id = "cus_123"
        
        mock_company_repository.get_by_id = AsyncMock(return_value=existing_company)
        mock_company_repository.get_by_name = AsyncMock(return_value=None)
        mock_company_repository.update = AsyncMock()
        
        mock_asaas_customers = MagicMock()
        mock_asaas_customers_instance = MagicMock()
        mock_asaas_customers.return_value = mock_asaas_customers_instance
        
        update_data = {"name": "New Name"}
        
        # Execute
        result = await company_service.update_company(update_data, company_id, mock_asaas_customers)
        
        # Assert
        assert result.name == "New Name"
        mock_company_repository.update.assert_called_once()
        mock_asaas_customers_instance.update_customer.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_company_not_found(self, company_service, mock_company_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=None)
        
        with pytest.raises(CompanyNotFound):
            await company_service.update_company({}, 999, MagicMock())

    @pytest.mark.asyncio
    async def test_update_company_name_already_exists(self, company_service, mock_company_repository):
        company_id = 1
        existing_company = MagicMock(spec=Company)
        existing_company.id = company_id
        existing_company.name = "Old Name"
        
        mock_company_repository.get_by_id = AsyncMock(return_value=existing_company)
        mock_company_repository.get_by_name = AsyncMock(return_value=MagicMock())
        
        with pytest.raises(NameAlreadyExists):
            await company_service.update_company({"name": "New Name"}, company_id, MagicMock())

    @pytest.mark.asyncio
    async def test_update_company_cnpj_already_exists(self, company_service, mock_company_repository):
        company_id = 1
        existing_company = MagicMock(spec=Company)
        existing_company.id = company_id
        existing_company.cnpj = "12345678000199"
        
        mock_company_repository.get_by_id = AsyncMock(return_value=existing_company)
        mock_company_repository.get_by_document = AsyncMock(return_value=MagicMock())
        
        with pytest.raises(CnpjAlreadyExists):
            await company_service.update_company({"cnpj": "88888888000188"}, company_id, MagicMock())

    @pytest.mark.asyncio
    async def test_update_company_plan_not_found(self, company_service, mock_company_repository, mock_plan_repository):
        company_id = 1
        existing_company = MagicMock(spec=Company)
        existing_company.id = company_id
        existing_company.plan_id = 1
        
        mock_company_repository.get_by_id = AsyncMock(return_value=existing_company)
        mock_plan_repository.get_by_id = AsyncMock(return_value=None)
        
        with pytest.raises(PlanNotFound):
            await company_service.update_company({"plan_id": 2}, company_id, MagicMock())

    @pytest.mark.asyncio
    async def test_update_company_all_fields(self, company_service, mock_company_repository, mock_plan_repository):
        company_id = 1
        existing_company = MagicMock(spec=Company)
        existing_company.id = company_id
        existing_company.customer_id = "cus_123"
        
        mock_company_repository.get_by_id = AsyncMock(return_value=existing_company)
        mock_company_repository.update = AsyncMock()
        mock_plan_repository.get_by_id = AsyncMock(return_value=MagicMock())

        mock_asaas_customers = MagicMock()
        mock_asaas_customers_instance = MagicMock()
        mock_asaas_customers.return_value = mock_asaas_customers_instance

        update_data = {
            "email": "new@email.com",
            "photo": "new_photo.png",
            "address": "new address",
            "number": 200,
            "state": "RJ",
            "cep": "00000-000",
            "city": "Rio",
            "phone": "21999999999",
            "whatsapp": "21999999999",
            "website": "www.new.com",
            "is_blocked": True,
            "plan_id": 2
        }
        
        await company_service.update_company(update_data, company_id, mock_asaas_customers)
        
        assert existing_company.email == "new@email.com"
        assert existing_company.is_blocked is True
        mock_company_repository.update.assert_called_once()

class TestCompanyServiceDelete:
    @pytest.mark.asyncio
    async def test_delete_company_success(self, company_service, mock_company_repository):
        company_id = 1
        existing_company = MagicMock(spec=Company)
        existing_company.customer_id = "cus_123"
        mock_company_repository.get_by_id = AsyncMock(return_value=existing_company)
        mock_company_repository.delete = AsyncMock()
        
        mock_asaas_customers = MagicMock()
        mock_asaas_customers_instance = MagicMock()
        mock_asaas_customers.return_value = mock_asaas_customers_instance
        
        mock_asaas_subscriptions = MagicMock()
        
        await company_service.delete_company(company_id, mock_asaas_customers, mock_asaas_subscriptions)
        
        mock_company_repository.delete.assert_called_once_with(company_id)
        mock_asaas_customers_instance.delete_customer.assert_called_once_with({"id": "cus_123"})

    @pytest.mark.asyncio
    async def test_delete_company_not_found(self, company_service, mock_company_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=None)
        
        with pytest.raises(CompanyNotFound):
            await company_service.delete_company(999, MagicMock(), MagicMock())
