import pytest
from unittest.mock import AsyncMock, MagicMock
from api.repositories.materials import MaterialRepository
from api.models.materials import Material

class TestMaterialRepository:
    @pytest.mark.asyncio
    async def test_save_material_success(self, mock_db_session):
        mock_material = MagicMock(spec=Material)
        repository = MaterialRepository(mock_db_session)
        
        result = await repository.save(mock_material)
        
        mock_db_session.add.assert_called_once_with(mock_material)
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_material)
        assert result == mock_material

    @pytest.mark.asyncio
    async def test_get_by_company_id_success(self, mock_db_session):
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = MaterialRepository(mock_db_session)
        
        result = await repository.get_by_company_id(1, 0, 20, None, None)
        
        assert result == []
        mock_db_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_company_id_with_filters(self, mock_db_session):
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = MaterialRepository(mock_db_session)
        
        await repository.get_by_company_id(1, 0, 20, "Steel", "Supplier")
        
        assert mock_db_session.execute.called

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, mock_db_session):
        mock_material = MagicMock(spec=Material)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_material
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = MaterialRepository(mock_db_session)
        
        result = await repository.get_by_id(1, 1)
        
        assert result == mock_material
        mock_db_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, mock_db_session):
        mock_db_session.execute = AsyncMock()
        repository = MaterialRepository(mock_db_session)
        
        await repository.delete_by_id(1, 1)
        
        mock_db_session.execute.assert_called_once()
        mock_db_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_success(self, mock_db_session):
        mock_material = MagicMock(spec=Material)
        mock_db_session.merge = AsyncMock()
        repository = MaterialRepository(mock_db_session)
        
        result = await repository.update(mock_material)
        
        mock_db_session.merge.assert_called_once_with(mock_material)
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_material)
        assert result == mock_material
