import pytest
from unittest.mock import AsyncMock, MagicMock
from api.services.clients import ClientService
from api.schemas.clients import ClientSchema
from api.models.legal_entitys import Client, LegalEntity
from api.exceptions.companys import CompanyNotFound
from api.exceptions.clients import ClientNotFound, ClientAccesDenied

@pytest.fixture
def mock_legal_entity_repository():
    return MagicMock()

@pytest.fixture
def mock_client_repository():
    return MagicMock()

@pytest.fixture
def mock_company_repository():
    return MagicMock()

@pytest.fixture
def client_service(mock_legal_entity_repository, mock_client_repository, mock_company_repository):
    return ClientService(mock_legal_entity_repository, mock_client_repository, mock_company_repository)

@pytest.fixture
def sample_client_schema():
    return ClientSchema(
        company_id=1,
        companie="Test Client",
        cpf_cnpj="00000000000191",
        email="client@test.com",
        phone="11999999999",
        address="Client Address",
        number=100,
        state="SP",
        cep="12345-678",
        city="Sao Paulo"
    )

class TestClientServiceCreate:
    @pytest.mark.asyncio
    async def test_create_client_success(self, client_service, mock_company_repository, mock_legal_entity_repository, mock_client_repository, sample_client_schema):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_legal_entity_repository.save = AsyncMock()
        mock_client_repository.save = AsyncMock()
        
        mock_client = MagicMock()
        mock_client_repository.get_by_id = AsyncMock(return_value=mock_client)
        
        result = await client_service.create(sample_client_schema)
        
        assert result == mock_client
        mock_company_repository.get_by_id.assert_called_once_with(1)
        mock_legal_entity_repository.save.assert_called_once()
        mock_client_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_client_company_not_found(self, client_service, mock_company_repository, sample_client_schema):
        mock_company_repository.get_by_id = AsyncMock(return_value=None)
        
        with pytest.raises(CompanyNotFound):
            await client_service.create(sample_client_schema)

class TestClientServiceList:
    @pytest.mark.asyncio
    async def test_list_clients_success(self, client_service, mock_company_repository, mock_client_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_client_repository.get_by_company_id = AsyncMock(return_value=[])
        
        result = await client_service.list(company_id=1)
        
        assert result == []
        mock_client_repository.get_by_company_id.assert_called_once()

class TestClientServiceGet:
    @pytest.mark.asyncio
    async def test_get_client_success(self, client_service, mock_company_repository, mock_client_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_client = MagicMock()
        mock_client_repository.get_by_id_and_company = AsyncMock(return_value=mock_client)
        
        result = await client_service.get(company_id=1, client_id=1)
        
        assert result == mock_client

    @pytest.mark.asyncio
    async def test_get_client_not_found(self, client_service, mock_company_repository, mock_client_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_client_repository.get_by_id_and_company = AsyncMock(return_value=None)
        
        with pytest.raises(ClientNotFound):
            await client_service.get(company_id=1, client_id=1)

class TestClientServiceDelete:
    @pytest.mark.asyncio
    async def test_delete_client_success(self, client_service, mock_company_repository, mock_client_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_client_repository.get_by_id_and_company = AsyncMock(return_value=MagicMock())
        mock_client_repository.delete_by_id = AsyncMock()
        
        await client_service.delete(company_id=1, client_id=1)
        
        mock_client_repository.delete_by_id.assert_called_once_with(1, 1)

class TestClientServiceUpdate:
    @pytest.mark.asyncio
    async def test_update_client_success(self, client_service, mock_company_repository, mock_client_repository, mock_legal_entity_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        
        existing_client = MagicMock()
        existing_client.company_id = 1
        existing_legal_entity = MagicMock()
        existing_client.legal_entity = existing_legal_entity
        
        mock_client_repository.get_by_id_and_company = AsyncMock(side_effect=[existing_client, existing_client])
        mock_legal_entity_repository.update = AsyncMock()
        
        update_data = {
            "company_id": 1,
            "companie": "New Name",
            "cpf_cnpj": "123",
            "email": "new@email.com",
            "phone": "123",
            "address": "new addr",
            "number": 200,
            "state": "RJ",
            "cep": "000",
            "city": "Rio"
        }
        
        result = await client_service.update(client_id=1, client_data=update_data)
        
        assert result == existing_client
        mock_legal_entity_repository.update.assert_called_once()
        assert existing_legal_entity.companie == "New Name"

    @pytest.mark.asyncio
    async def test_update_client_access_denied(self, client_service, mock_company_repository, mock_client_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        
        existing_client = MagicMock()
        existing_client.company_id = 1
        
        mock_client_repository.get_by_id_and_company = AsyncMock(return_value=existing_client)
        
        with pytest.raises(ClientAccesDenied):
            await client_service.update(client_id=1, client_data={"company_id": 2})
