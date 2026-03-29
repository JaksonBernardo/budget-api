"""Testes para repositories de segmentos"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.segments import SegmentRepository
from api.models.segments import Segment


class TestSegmentRepositorySave:
    """Testes para método save do SegmentRepository"""

    @pytest.mark.asyncio
    async def test_save_segment_success(self, mock_db_session, sample_segment_model):
        """Testa salvamento de segmento com sucesso"""
        mock_db_session.add = AsyncMock()
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()

        repository = SegmentRepository(mock_db_session)
        result = await repository.save(sample_segment_model)

        mock_db_session.add.assert_called_once_with(sample_segment_model)
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(sample_segment_model)
        assert result == sample_segment_model

    @pytest.mark.asyncio
    async def test_save_segment_rollback_on_error(self, mock_db_session, sample_segment_model):
        """Testa que rollback é chamado em caso de erro"""
        mock_db_session.add = AsyncMock()
        mock_db_session.commit = AsyncMock(side_effect=Exception("DB Error"))
        mock_db_session.rollback = AsyncMock()

        repository = SegmentRepository(mock_db_session)

        with pytest.raises(Exception):
            await repository.save(sample_segment_model)

        mock_db_session.rollback.assert_called_once()


class TestSegmentRepositoryGetByCompanyId:
    """Testes para método get_by_company_id do SegmentRepository"""

    @pytest.mark.asyncio
    async def test_get_segments_by_company_id_success(self, mock_db_session):
        """Testa obtenção de segmentos por company_id com sucesso"""
        mock_segment_1 = MagicMock()
        mock_segment_1.id = 1
        mock_segment_1.name = "Segmento 1"
        mock_segment_2 = MagicMock()
        mock_segment_2.id = 2
        mock_segment_2.name = "Segmento 2"
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_segment_1, mock_segment_2]
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        repository = SegmentRepository(mock_db_session)
        result = await repository.get_by_company_id(company_id=1, offset=0, limit=20, search=None)

        assert len(result) == 2
        assert result[0].name == "Segmento 1"
        mock_db_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_segments_by_company_id_with_search(self, mock_db_session):
        """Testa obtenção de segmentos com busca por nome"""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        repository = SegmentRepository(mock_db_session)
        await repository.get_by_company_id(company_id=1, offset=0, limit=20, search="teste")

        mock_db_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_segments_empty_result(self, mock_db_session):
        """Testa obtenção de segmentos quando não há resultados"""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        repository = SegmentRepository(mock_db_session)
        result = await repository.get_by_company_id(company_id=1, offset=0, limit=20, search=None)

        assert result == []


class TestSegmentRepositoryGetById:
    """Testes para método get_by_id do SegmentRepository"""

    @pytest.mark.asyncio
    async def test_get_segment_by_id_success(self, mock_db_session, sample_segment_model):
        """Testa obtenção de segmento por id com sucesso"""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_segment_model
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        repository = SegmentRepository(mock_db_session)
        result = await repository.get_by_id(company_id=1, segment_id=1)

        assert result is not None
        assert result.id == sample_segment_model.id
        mock_db_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_segment_by_id_not_found(self, mock_db_session):
        """Testa obtenção de segmento quando não encontrado"""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        repository = SegmentRepository(mock_db_session)
        result = await repository.get_by_id(company_id=1, segment_id=999)

        assert result is None


class TestSegmentRepositoryDeleteById:
    """Testes para método delete_by_id do SegmentRepository"""

    @pytest.mark.asyncio
    async def test_delete_segment_by_id_success(self, mock_db_session):
        """Testa exclusão de segmento por id com sucesso"""
        mock_db_session.execute = AsyncMock()
        mock_db_session.commit = AsyncMock()

        repository = SegmentRepository(mock_db_session)
        await repository.delete_by_id(company_id=1, segment_id=1)

        mock_db_session.execute.assert_called_once()
        mock_db_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_segment_by_id_rollback_on_error(self, mock_db_session):
        """Testa que rollback é chamado em caso de erro na exclusão"""
        mock_db_session.execute = AsyncMock()
        mock_db_session.commit = AsyncMock(side_effect=Exception("DB Error"))
        mock_db_session.rollback = AsyncMock()

        repository = SegmentRepository(mock_db_session)

        with pytest.raises(Exception):
            await repository.delete_by_id(company_id=1, segment_id=1)

        mock_db_session.rollback.assert_called_once()


class TestSegmentRepositoryUpdate:
    """Testes para método update do SegmentRepository"""

    @pytest.mark.asyncio
    async def test_update_segment_success(self, mock_db_session, sample_segment_model):
        """Testa atualização de segmento com sucesso"""
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()

        repository = SegmentRepository(mock_db_session)
        result = await repository.update(sample_segment_model)

        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(sample_segment_model)
        assert result == sample_segment_model

    @pytest.mark.asyncio
    async def test_update_segment_rollback_on_error(self, mock_db_session, sample_segment_model):
        """Testa que rollback é chamado em caso de erro na atualização"""
        mock_db_session.commit = AsyncMock(side_effect=Exception("DB Error"))
        mock_db_session.rollback = AsyncMock()

        repository = SegmentRepository(mock_db_session)

        with pytest.raises(Exception):
            await repository.update(sample_segment_model)

        mock_db_session.rollback.assert_called_once()
