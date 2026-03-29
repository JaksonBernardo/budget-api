"""Testes para services de segmentos"""
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, call

from api.services.segments.service import SegmentService
from api.exceptions.segments import (
    SegmentInvalidName,
    SegmentNotFound,
    SegmentAccesDenied,
)
from api.exceptions.companys import CompanyNotFound


class TestSegmentServiceCreate:
    """Testes para método create do SegmentService"""

    @pytest.mark.asyncio
    async def test_create_segment_success(
        self, mock_segment_repository, mock_company_repository,
        sample_segment_data, sample_company_model
    ):
        """Testa criação de segmento com sucesso"""
        mock_company_repository.get_by_id = AsyncMock(return_value=sample_company_model)
        saved_segment = MagicMock()
        saved_segment.id = 1
        saved_segment.name = sample_segment_data["name"]
        saved_segment.contract = sample_segment_data["contract"]
        saved_segment.company_id = sample_segment_data["company_id"]
        saved_segment.created_at = datetime.now()
        saved_segment.updated_at = datetime.now()
        mock_segment_repository.save = AsyncMock(return_value=saved_segment)

        service = SegmentService(mock_segment_repository, mock_company_repository)
        segment_data = MagicMock()
        segment_data.name = sample_segment_data["name"]
        segment_data.contract = sample_segment_data["contract"]
        segment_data.company_id = sample_segment_data["company_id"]
        result = await service.create(segment_data)

        assert result is not None
        assert result.name == sample_segment_data["name"]
        mock_company_repository.get_by_id.assert_called_once_with(sample_segment_data["company_id"])
        mock_segment_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_segment_company_not_found(
        self, mock_segment_repository, mock_company_repository,
        sample_segment_data
    ):
        """Testa que criação de segmento lança CompanyNotFound quando empresa não existe"""
        mock_company_repository.get_by_id = AsyncMock(return_value=None)

        service = SegmentService(mock_segment_repository, mock_company_repository)

        with pytest.raises(CompanyNotFound):
            await service.create(MagicMock(**sample_segment_data))

        mock_company_repository.get_by_id.assert_called_once_with(sample_segment_data["company_id"])
        mock_segment_repository.save.assert_not_called()


class TestSegmentServiceList:
    """Testes para método list do SegmentService"""

    @pytest.mark.asyncio
    async def test_list_segments_success(
        self, mock_segment_repository, mock_company_repository,
        sample_company_model
    ):
        """Testa listagem de segmentos com sucesso"""
        mock_company_repository.get_by_id = AsyncMock(return_value=sample_company_model)
        mock_segment_1 = MagicMock()
        mock_segment_1.id = 1
        mock_segment_1.name = "Segmento 1"
        mock_segment_2 = MagicMock()
        mock_segment_2.id = 2
        mock_segment_2.name = "Segmento 2"
        mock_segment_repository.get_by_company_id = AsyncMock(return_value=[mock_segment_1, mock_segment_2])

        service = SegmentService(mock_segment_repository, mock_company_repository)
        result = await service.list(company_id=1, offset=0, limit=20, search=None)

        assert len(result) == 2
        assert result[0].name == "Segmento 1"
        mock_segment_repository.get_by_company_id.assert_called_once_with(1, 0, 20, None)

    @pytest.mark.asyncio
    async def test_list_segments_with_search(
        self, mock_segment_repository, mock_company_repository,
        sample_company_model
    ):
        """Testa listagem de segmentos com busca"""
        mock_company_repository.get_by_id = AsyncMock(return_value=sample_company_model)
        mock_segment_repository.get_by_company_id = AsyncMock(return_value=[])

        service = SegmentService(mock_segment_repository, mock_company_repository)
        await service.list(company_id=1, offset=0, limit=20, search="teste")

        mock_segment_repository.get_by_company_id.assert_called_once_with(1, 0, 20, "%teste%")

    @pytest.mark.asyncio
    async def test_list_segments_company_not_found(
        self, mock_segment_repository, mock_company_repository
    ):
        """Testa que listagem lança CompanyNotFound quando empresa não existe"""
        mock_company_repository.get_by_id = AsyncMock(return_value=None)

        service = SegmentService(mock_segment_repository, mock_company_repository)

        with pytest.raises(CompanyNotFound):
            await service.list(company_id=999, offset=0, limit=20, search=None)


class TestSegmentServiceGet:
    """Testes para método get do SegmentService"""

    @pytest.mark.asyncio
    async def test_get_segment_success(
        self, mock_segment_repository, mock_company_repository,
        sample_company_model, sample_segment_model
    ):
        """Testa obtenção de segmento com sucesso"""
        mock_company_repository.get_by_id = AsyncMock(return_value=sample_company_model)
        mock_segment_repository.get_by_id = AsyncMock(return_value=sample_segment_model)

        service = SegmentService(mock_segment_repository, mock_company_repository)
        result = await service.get(company_id=1, segment_id=1)

        assert result is not None
        assert result.id == sample_segment_model.id
        mock_segment_repository.get_by_id.assert_called_once_with(1, 1)

    @pytest.mark.asyncio
    async def test_get_segment_company_not_found(
        self, mock_segment_repository, mock_company_repository
    ):
        """Testa que obtenção lança CompanyNotFound quando empresa não existe"""
        mock_company_repository.get_by_id = AsyncMock(return_value=None)

        service = SegmentService(mock_segment_repository, mock_company_repository)

        with pytest.raises(CompanyNotFound):
            await service.get(company_id=999, segment_id=1)

    @pytest.mark.asyncio
    async def test_get_segment_not_found(
        self, mock_segment_repository, mock_company_repository,
        sample_company_model
    ):
        """Testa que obtenção lança SegmentNotFound quando segmento não existe"""
        mock_company_repository.get_by_id = AsyncMock(return_value=sample_company_model)
        mock_segment_repository.get_by_id = AsyncMock(return_value=None)

        service = SegmentService(mock_segment_repository, mock_company_repository)

        with pytest.raises(SegmentNotFound):
            await service.get(company_id=1, segment_id=999)


class TestSegmentServiceDelete:
    """Testes para método delete do SegmentService"""

    @pytest.mark.asyncio
    async def test_delete_segment_success(
        self, mock_segment_repository, mock_company_repository,
        sample_company_model, sample_segment_model
    ):
        """Testa exclusão de segmento com sucesso"""
        mock_company_repository.get_by_id = AsyncMock(return_value=sample_company_model)
        mock_segment_repository.get_by_id = AsyncMock(return_value=sample_segment_model)
        mock_segment_repository.delete_by_id = AsyncMock()

        service = SegmentService(mock_segment_repository, mock_company_repository)
        await service.delete(company_id=1, segment_id=1)

        mock_segment_repository.delete_by_id.assert_called_once_with(1, 1)

    @pytest.mark.asyncio
    async def test_delete_segment_not_found(
        self, mock_segment_repository, mock_company_repository,
        sample_company_model
    ):
        """Testa que exclusão lança SegmentNotFound quando segmento não existe"""
        mock_company_repository.get_by_id = AsyncMock(return_value=sample_company_model)
        mock_segment_repository.get_by_id = AsyncMock(return_value=None)

        service = SegmentService(mock_segment_repository, mock_company_repository)

        with pytest.raises(SegmentNotFound):
            await service.delete(company_id=1, segment_id=999)


class TestSegmentServiceUpdate:
    """Testes para método update do SegmentService"""

    @pytest.mark.asyncio
    async def test_update_segment_success(
        self, mock_segment_repository, mock_company_repository,
        sample_company_model, sample_segment_model
    ):
        """Testa atualização de segmento com sucesso"""
        mock_company_repository.get_by_id = AsyncMock(return_value=sample_company_model)
        mock_segment_repository.get_by_id = AsyncMock(return_value=sample_segment_model)
        mock_segment_repository.update = AsyncMock(return_value=sample_segment_model)

        service = SegmentService(mock_segment_repository, mock_company_repository)
        update_data = {
            "name": "Nome Atualizado",
            "company_id": 1,
            "contract": "Contrato Atualizado",
        }
        result = await service.update(segment_id=1, segment_data=update_data)

        assert result is not None
        mock_segment_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_segment_invalid_name(
        self, mock_segment_repository, mock_company_repository,
        sample_company_model, sample_segment_model
    ):
        """Testa que atualização com nome vazio lança SegmentInvalidName"""
        mock_company_repository.get_by_id = AsyncMock(return_value=sample_company_model)
        mock_segment_repository.get_by_id = AsyncMock(return_value=sample_segment_model)

        service = SegmentService(mock_segment_repository, mock_company_repository)
        update_data = {
            "name": "",
            "company_id": 1,
        }

        with pytest.raises(SegmentInvalidName):
            await service.update(segment_id=1, segment_data=update_data)

    @pytest.mark.asyncio
    async def test_update_segment_access_denied(
        self, mock_segment_repository, mock_company_repository,
        sample_company_model, sample_segment_model
    ):
        """Testa que atualização com company_id diferente lança SegmentAccesDenied"""
        mock_company_repository.get_by_id = AsyncMock(return_value=sample_company_model)
        sample_segment_model.company_id = 1
        mock_segment_repository.get_by_id = AsyncMock(return_value=sample_segment_model)

        service = SegmentService(mock_segment_repository, mock_company_repository)
        update_data = {
            "name": "Nome Atualizado",
            "company_id": 2,  # Diferente do original
        }

        with pytest.raises(SegmentAccesDenied):
            await service.update(segment_id=1, segment_data=update_data)
