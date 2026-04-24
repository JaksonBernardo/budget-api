import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from api.services.materials import MaterialService
from api.schemas.materials import MaterialSchema
from api.models.materials import Material
from api.exceptions import (
    CompanyNotFound,
    MaterialNotFound,
    SupplierNotFound
)

@pytest.fixture
def mock_material_repository():
    return MagicMock()

@pytest.fixture
def mock_supplier_repository():
    return MagicMock()

@pytest.fixture
def mock_company_repository():
    return MagicMock()

@pytest.fixture
def material_service(mock_material_repository, mock_supplier_repository, mock_company_repository):
    return MaterialService(mock_material_repository, mock_supplier_repository, mock_company_repository)

@pytest.fixture
def sample_material_schema():
    return MaterialSchema(
        name="Steel",
        unit_cost=10.0,
        classification="DIRECT",
        supplier_id=1,
        company_id=1
    )

class TestMaterialService:
    @pytest.mark.asyncio
    async def test_create_material_success(self, material_service, mock_company_repository, mock_supplier_repository, mock_material_repository, sample_material_schema):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_supplier_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_material = MagicMock(spec=Material)
        mock_material_repository.save = AsyncMock(return_value=mock_material)

        result = await material_service.create(sample_material_schema)

        assert result == mock_material
        mock_company_repository.get_by_id.assert_called_once_with(1)
        mock_supplier_repository.get_by_id.assert_called_once_with(1)
        mock_material_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_material_company_not_found(self, material_service, mock_company_repository, sample_material_schema):
        mock_company_repository.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(CompanyNotFound):
            await material_service.create(sample_material_schema)

    @pytest.mark.asyncio
    async def test_create_material_supplier_not_found(self, material_service, mock_company_repository, mock_supplier_repository, sample_material_schema):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_supplier_repository.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(SupplierNotFound):
            await material_service.create(sample_material_schema)

    @pytest.mark.asyncio
    async def test_list_materials_success(self, material_service, mock_company_repository, mock_material_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_material_repository.get_by_company_id = AsyncMock(return_value=[])

        result = await material_service.list(company_id=1)

        assert result == []
        mock_material_repository.get_by_company_id.assert_called_once_with(1, 0, 20, None, None)

    @pytest.mark.asyncio
    async def test_get_material_success(self, material_service, mock_company_repository, mock_material_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_material = MagicMock(spec=Material)
        mock_material_repository.get_by_id = AsyncMock(return_value=mock_material)

        result = await material_service.get(1, 1)

        assert result == mock_material

    @pytest.mark.asyncio
    async def test_delete_material_success(self, material_service, mock_company_repository, mock_material_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_material_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_material_repository.delete_by_id = AsyncMock()

        await material_service.delete(1, 1)

        mock_material_repository.delete_by_id.assert_called_once_with(1, 1)

    @pytest.mark.asyncio
    async def test_update_material_success(self, material_service, mock_company_repository, mock_supplier_repository, mock_material_repository):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_supplier_repository.get_by_id = AsyncMock(return_value=MagicMock())
        existing_material = MagicMock(spec=Material)
        existing_material.company_id = 1
        mock_material_repository.get_by_id = AsyncMock(return_value=existing_material)
        mock_material_repository.update = AsyncMock(return_value=existing_material)

        update_data = {
            "company_id": 1,
            "supplier_id": 1,
            "name": "Updated Steel",
            "unit_cost": 15.0,
            "classification": "INDIRECT"
        }
        result = await material_service.update(1, update_data)

        assert result == existing_material
        assert existing_material.name == "Updated Steel"
        mock_material_repository.update.assert_called_once()
