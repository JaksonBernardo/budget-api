import pytest
from unittest.mock import AsyncMock, MagicMock
from api.repositories.suppliers import SupplierRepository
from api.models.legal_entitys import Supplier

class TestSupplierRepository:
    @pytest.mark.asyncio
    async def test_save_supplier_success(self, mock_db_session):
        mock_supplier = MagicMock(spec=Supplier)
        mock_db_session.flush = AsyncMock()
        repository = SupplierRepository(mock_db_session)
        
        result = await repository.save(mock_supplier)
        
        mock_db_session.add.assert_called_once_with(mock_supplier)
        mock_db_session.flush.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_supplier)
        assert result == mock_supplier

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, mock_db_session):
        mock_supplier = MagicMock(spec=Supplier)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_supplier
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = SupplierRepository(mock_db_session)
        
        result = await repository.get_by_id(1)
        
        assert result == mock_supplier

    @pytest.mark.asyncio
    async def test_get_by_company_id_success(self, mock_db_session):
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = SupplierRepository(mock_db_session)
        
        result = await repository.get_by_company_id(1, 0, 20, None)
        
        assert result == []

    @pytest.mark.asyncio
    async def test_get_by_id_and_company_success(self, mock_db_session):
        mock_supplier = MagicMock(spec=Supplier)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_supplier
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = SupplierRepository(mock_db_session)
        
        result = await repository.get_by_id_and_company(1, 1)
        
        assert result == mock_supplier

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, mock_db_session):
        mock_supplier = MagicMock(spec=Supplier)
        mock_supplier.legal_entity = MagicMock()
        mock_supplier.legal_entity.id = 1
        
        # We need to mock get_by_id_and_company because delete_by_id calls it
        repository = SupplierRepository(mock_db_session)
        repository.get_by_id_and_company = AsyncMock(return_value=mock_supplier)
        
        mock_db_session.execute = AsyncMock()
        
        await repository.delete_by_id(1, 1)
        
        assert mock_db_session.execute.called
        mock_db_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_success(self, mock_db_session):
        mock_supplier = MagicMock(spec=Supplier)
        mock_db_session.merge = AsyncMock()
        repository = SupplierRepository(mock_db_session)
        
        result = await repository.update(mock_supplier)
        
        mock_db_session.merge.assert_called_once_with(mock_supplier)
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_supplier)
        assert result == mock_supplier
