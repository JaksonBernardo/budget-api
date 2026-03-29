"""Testes de integração para endpoints de segmentos"""
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime


@pytest.fixture
async def test_client():
    """Cria um cliente de teste usando ASGITransport"""
    from api.app import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


class TestSegmentEndpoints:
    """Testes de integração para endpoints de segmentos"""

    @pytest.mark.asyncio
    async def test_health_check(self, test_client: AsyncClient):
        """Testa endpoint de health check"""
        response = await test_client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "OK.."}

    @pytest.mark.asyncio
    async def test_list_segments_success(self, test_client: AsyncClient, sample_segment_model):
        """Testa listagem de segmentos com sucesso"""
        with patch("api.services.segments.service.SegmentService.list", new_callable=AsyncMock) as mock_list:
            mock_list.return_value = [sample_segment_model]

            response = await test_client.get("/api/segments/1")

            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_list_segments_with_pagination(self, test_client: AsyncClient):
        """Testa listagem de segmentos com paginação"""
        with patch("api.services.segments.service.SegmentService.list", new_callable=AsyncMock) as mock_list:
            mock_list.return_value = []

            response = await test_client.get("/api/segments/1?offset=10&limit=5")

            assert response.status_code == 200
            mock_list.assert_called_once_with(1, 10, 5, None)

    @pytest.mark.asyncio
    async def test_list_segments_with_search(self, test_client: AsyncClient):
        """Testa listagem de segmentos com busca"""
        with patch("api.services.segments.service.SegmentService.list", new_callable=AsyncMock) as mock_list:
            mock_list.return_value = []

            response = await test_client.get("/api/segments/1?search=teste")

            assert response.status_code == 200
            mock_list.assert_called_once_with(1, 0, 20, "teste")

    @pytest.mark.asyncio
    async def test_get_segment_success(self, test_client: AsyncClient, sample_segment_model):
        """Testa obtenção de segmento específico com sucesso"""
        with patch("api.services.segments.service.SegmentService.get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = sample_segment_model
            mock_get.return_value.model_dump = MagicMock(return_value={
                "id": sample_segment_model.id,
                "name": sample_segment_model.name,
                "contract": sample_segment_model.contract,
                "company_id": sample_segment_model.company_id,
                "created_at": sample_segment_model.created_at,
                "updated_at": sample_segment_model.updated_at,
            })

            response = await test_client.get("/api/segments/1/1")

            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_segment_not_found(self, test_client: AsyncClient):
        """Testa obtenção de segmento não encontrado"""
        with patch("api.services.segments.service.SegmentService.get", new_callable=AsyncMock) as mock_get:
            from api.exceptions.segments import SegmentNotFound
            mock_get.side_effect = SegmentNotFound()

            response = await test_client.get("/api/segments/1/999")

            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_segment_success(self, test_client: AsyncClient):
        """Testa exclusão de segmento com sucesso"""
        with patch("api.services.segments.service.SegmentService.delete", new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = None

            response = await test_client.delete("/api/segments/1/1")

            assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_segment_not_found(self, test_client: AsyncClient):
        """Testa exclusão de segmento não encontrado"""
        with patch("api.services.segments.service.SegmentService.delete", new_callable=AsyncMock) as mock_delete:
            from api.exceptions.segments import SegmentNotFound
            mock_delete.side_effect = SegmentNotFound()

            response = await test_client.delete("/api/segments/1/999")

            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_segments_company_not_found(self, test_client: AsyncClient):
        """Testa listagem de segmentos com empresa não encontrada"""
        with patch("api.services.segments.service.SegmentService.list", new_callable=AsyncMock) as mock_list:
            from api.exceptions.companys import CompanyNotFound
            mock_list.side_effect = CompanyNotFound()

            response = await test_client.get("/api/segments/999")

            assert response.status_code == 404
