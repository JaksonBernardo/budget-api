"""Testes para repositories de empresas"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from api.repositories.companys import CompanyRepository
from api.models.companys import Company

class TestCompanyRepository:
    @pytest.mark.asyncio
    async def test_create_company_success(self, mock_db_session):
        mock_company = MagicMock(spec=Company)
        mock_db_session.flush = AsyncMock()
        repository = CompanyRepository(mock_db_session)
        
        result = await repository.create(mock_company)
        
        mock_db_session.add.assert_called_once_with(mock_company)
        mock_db_session.flush.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_company)
        assert result == mock_company

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, mock_db_session):
        mock_company = MagicMock(spec=Company)
        mock_db_session.scalar = AsyncMock(return_value=mock_company)
        repository = CompanyRepository(mock_db_session)
        
        result = await repository.get_by_id(1)
        
        assert result == mock_company
        mock_db_session.scalar.assert_called_once()

    @pytest.mark.asyncio
    async def test_verify_if_plan_id_exists(self, mock_db_session):
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [MagicMock()]
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = CompanyRepository(mock_db_session)
        
        result = await repository.verify_if_plan_id(1)
        
        assert result is True

    @pytest.mark.asyncio
    async def test_verify_if_plan_id_not_exists(self, mock_db_session):
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = CompanyRepository(mock_db_session)
        
        result = await repository.verify_if_plan_id(1)
        
        assert result is False

    @pytest.mark.asyncio
    async def test_get_all_success(self, mock_db_session):
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = CompanyRepository(mock_db_session)
        
        result = await repository.get_all(limit=10, offset=0, search=None)
        
        assert result == []
        mock_db_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_with_search(self, mock_db_session):
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = CompanyRepository(mock_db_session)
        
        await repository.get_all(limit=10, offset=0, search="test")
        
        mock_db_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_name_success(self, mock_db_session):
        mock_company = MagicMock(spec=Company)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_company
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = CompanyRepository(mock_db_session)
        
        result = await repository.get_by_name("Test Company")
        
        assert result == mock_company
        mock_db_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_document_success(self, mock_db_session):
        mock_company = MagicMock(spec=Company)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_company
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = CompanyRepository(mock_db_session)
        
        result = await repository.get_by_document("12345678000199")
        
        assert result == mock_company
        mock_db_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_success(self, mock_db_session):
        mock_db_session.execute = AsyncMock()
        mock_db_session.commit = AsyncMock()
        repository = CompanyRepository(mock_db_session)
        
        await repository.delete(1)
        
        mock_db_session.execute.assert_called_once()
        mock_db_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_success(self, mock_db_session):
        mock_company = MagicMock(spec=Company)
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        repository = CompanyRepository(mock_db_session)
        
        result = await repository.update(mock_company)
        
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_company)
        assert result == mock_company
