import pytest
from unittest.mock import AsyncMock, MagicMock
from api.repositories.clients import ClientRepository
from api.models.legal_entitys import Client

class TestClientRepository:
    @pytest.mark.asyncio
    async def test_save_client_success(self, mock_db_session):
        mock_client = MagicMock(spec=Client)
        mock_db_session.flush = AsyncMock()
        repository = ClientRepository(mock_db_session)
        
        result = await repository.save(mock_client)
        
        mock_db_session.add.assert_called_once_with(mock_client)
        mock_db_session.flush.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_client)
        assert result == mock_client

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, mock_db_session):
        mock_client = MagicMock(spec=Client)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_client
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = ClientRepository(mock_db_session)
        
        result = await repository.get_by_id(1)
        
        assert result == mock_client

    @pytest.mark.asyncio
    async def test_get_by_id_and_company_success(self, mock_db_session):
        mock_client = MagicMock(spec=Client)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_client
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = ClientRepository(mock_db_session)
        
        result = await repository.get_by_id_and_company(1, 1)
        
        assert result == mock_client

    @pytest.mark.asyncio
    async def test_update_success(self, mock_db_session):
        mock_client = MagicMock(spec=Client)
        mock_db_session.merge = AsyncMock()
        repository = ClientRepository(mock_db_session)
        
        result = await repository.update(mock_client)
        
        mock_db_session.merge.assert_called_once_with(mock_client)
        mock_db_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, mock_db_session):
        mock_client = MagicMock(spec=Client)
        mock_client.legal_entity = MagicMock()
        mock_client.legal_entity.id = 1
        
        repository = ClientRepository(mock_db_session)
        repository.get_by_id_and_company = AsyncMock(return_value=mock_client)
        
        mock_db_session.execute = AsyncMock()
        
        await repository.delete_by_id(1, 1)
        
        assert mock_db_session.execute.called
        mock_db_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_company_id_success(self, mock_db_session):
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = ClientRepository(mock_db_session)
        
        result = await repository.get_by_company_id(1, 0, 20, "search")
        
        assert result == []
