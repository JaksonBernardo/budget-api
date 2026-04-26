import pytest
from unittest.mock import AsyncMock, MagicMock
from api.services.suppliers import SupplierService
from api.schemas.suppliers import SupplierSchema
from api.models.legal_entitys import Supplier, LegalEntity
from api.exceptions import (
    CompanyNotFound,
    SupplierNotFound,
    SupplierAccesDenied
)

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_legal_entity_repository():
    return MagicMock()

@pytest.fixture
def mock_supplier_repository():
    return MagicMock()

@pytest.fixture
def mock_company_repository():
    return MagicMock()

@pytest.fixture
def supplier_service(mock_db, mock_legal_entity_repository, mock_supplier_repository, mock_company_repository):
    return SupplierService(mock_db, mock_legal_entity_repository, mock_supplier_repository, mock_company_repository)

@pytest.fixture
def sample_supplier_schema():
    return SupplierSchema(
        company_id=1,
        companie="Test Supplier",
        cpf_cnpj="00000000000191",
        email="supplier@test.com",
        phone="11999999999",
        address="Supplier Address",
        number=100,
        state="SP",
        cep="12345-678",
        city="Sao Paulo"
    )

class TestSupplierService:
    @pytest.mark.asyncio
    async def test_create_supplier_success(self, supplier_service, mock_company_repository, mock_legal_entity_repository, mock_supplier_repository, sample_supplier_schema):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_legal_entity_repository.save = AsyncMock()
        mock_supplier_repository.save = AsyncMock()
        mock_supplier = MagicMock()
        mock_supplier_repository.get_by_id = AsyncMock(return_value=mock_supplier)
        
        result = await supplier_service.create(sample_supplier_schema)
        
        assert result == mock_supplier
        mock_company_repository.get_by_id.assert_called_once_with(1)
        mock_legal_entity_repository.save.assert_called_once()
        mock_supplier_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_suppliers_success(self, supplier_service, mock_company_repository, mock_supplier_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_supplier_repository.get_by_company_id = AsyncMock(return_value=[])
        
        result = await supplier_service.list(company_id=1)
        
        assert result == []

    @pytest.mark.asyncio
    async def test_get_supplier_success(self, supplier_service, mock_company_repository, mock_supplier_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_supplier = MagicMock()
        mock_supplier_repository.get_by_id_and_company = AsyncMock(return_value=mock_supplier)
        
        result = await supplier_service.get(1, 1)
        
        assert result == mock_supplier

    @pytest.mark.asyncio
    async def test_delete_supplier_success(self, supplier_service, mock_company_repository, mock_supplier_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_supplier_repository.get_by_id_and_company = AsyncMock(return_value=MagicMock())
        mock_supplier_repository.delete_by_id = AsyncMock()
        
        await supplier_service.delete(1, 1)
        
        mock_supplier_repository.delete_by_id.assert_called_once_with(1, 1)

    @pytest.mark.asyncio
    async def test_update_supplier_success(self, supplier_service, mock_company_repository, mock_supplier_repository, mock_legal_entity_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        existing_supplier = MagicMock()
        existing_supplier.company_id = 1
        existing_supplier.legal_entity = MagicMock()
        mock_supplier_repository.get_by_id_and_company = AsyncMock(side_effect=[existing_supplier, existing_supplier])
        mock_legal_entity_repository.update = AsyncMock()
        
        update_data = {"company_id": 1, "companie": "Updated Supplier"}
        result = await supplier_service.update(1, update_data)
        
        assert result == existing_supplier
        mock_legal_entity_repository.update.assert_called_once()
