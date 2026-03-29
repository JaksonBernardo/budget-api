"""Testes para schemas de segmentos"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from api.schemas.segments import (
    SegmentSchema,
    SegmentPublicSchema,
    SegmentUpdateSchema,
    ListSegmentPublicSchema,
)
from api.exceptions.segments import SegmentInvalidName
from api.exceptions.companys import InvalidTypeCompanyId, ZeroCompanyId


class TestSegmentSchema:
    """Testes para SegmentSchema"""

    def test_create_segment_schema_valid(self, sample_segment_data):
        """Testa criação de schema com dados válidos"""
        schema = SegmentSchema(
            name=sample_segment_data["name"],
            contract=sample_segment_data["contract"],
            company_id=sample_segment_data["company_id"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        assert schema.name == sample_segment_data["name"]
        assert schema.contract == sample_segment_data["contract"]
        assert schema.company_id == sample_segment_data["company_id"]

    def test_create_segment_schema_with_empty_name(self, sample_segment_data):
        """Testa que schema com nome vazio lança exceção"""
        with pytest.raises(SegmentInvalidName):
            SegmentSchema(
                name="",
                contract=sample_segment_data["contract"],
                company_id=sample_segment_data["company_id"],
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

    def test_create_segment_schema_with_invalid_company_id_type(self, sample_segment_data):
        """Testa que schema com company_id inválido lança ValidationError do Pydantic"""
        with pytest.raises(ValidationError):
            SegmentSchema(
                name=sample_segment_data["name"],
                contract=sample_segment_data["contract"],
                company_id="invalid",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

    def test_create_segment_schema_with_zero_company_id(self, sample_segment_data):
        """Testa que schema com company_id zero lança exceção"""
        with pytest.raises(ZeroCompanyId):
            SegmentSchema(
                name=sample_segment_data["name"],
                contract=sample_segment_data["contract"],
                company_id=0,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

    def test_create_segment_schema_with_negative_company_id(self, sample_segment_data):
        """Testa que schema com company_id negativo lança exceção"""
        with pytest.raises(ZeroCompanyId):
            SegmentSchema(
                name=sample_segment_data["name"],
                contract=sample_segment_data["contract"],
                company_id=-1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

    def test_create_segment_schema_contract_optional(self, sample_segment_data):
        """Testa que contract é opcional"""
        schema = SegmentSchema(
            name=sample_segment_data["name"],
            contract=None,
            company_id=sample_segment_data["company_id"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        assert schema.contract is None


class TestSegmentPublicSchema:
    """Testes para SegmentPublicSchema"""

    def test_create_segment_public_schema(self, sample_segment_model):
        """Testa criação de schema público com dados válidos"""
        schema = SegmentPublicSchema(
            id=sample_segment_model.id,
            name=sample_segment_model.name,
            contract=sample_segment_model.contract,
            company_id=sample_segment_model.company_id,
            created_at=sample_segment_model.created_at,
            updated_at=sample_segment_model.updated_at,
        )

        assert schema.id == sample_segment_model.id
        assert schema.name == sample_segment_model.name
        assert schema.contract == sample_segment_model.contract


class TestSegmentUpdateSchema:
    """Testes para SegmentUpdateSchema"""

    def test_create_segment_update_schema_valid(self, sample_segment_data):
        """Testa criação de schema de atualização com dados válidos"""
        schema = SegmentUpdateSchema(
            name="Novo Nome",
            contract="Novo Contrato",
            company_id=sample_segment_data["company_id"],
            updated_at=datetime.now(),
        )

        assert schema.name == "Novo Nome"
        assert schema.contract == "Novo Contrato"

    def test_create_segment_update_schema_partial(self):
        """Testa que schema de atualização parcial não é permitido (todos campos required)"""
        # O schema exige todos os campos, mesmo sendo Optional
        with pytest.raises(ValidationError):
            SegmentUpdateSchema(name="Apenas Nome")

    def test_create_segment_update_schema_empty_name(self):
        """Testa que schema com nome vazio lança exceção"""
        with pytest.raises(SegmentInvalidName):
            SegmentUpdateSchema(name="", updated_at=datetime.now())

    def test_create_segment_update_schema_invalid_company_id(self):
        """Testa que schema com company_id inválido lança ValidationError do Pydantic"""
        with pytest.raises(ValidationError):
            SegmentUpdateSchema(company_id="invalid", updated_at=datetime.now())


class TestListSegmentPublicSchema:
    """Testes para ListSegmentPublicSchema"""

    def test_create_list_segment_schema(self, sample_segment_model):
        """Testa criação de schema de lista"""
        segments_data = [
            {
                "id": sample_segment_model.id,
                "name": sample_segment_model.name,
                "contract": sample_segment_model.contract,
                "company_id": sample_segment_model.company_id,
                "created_at": sample_segment_model.created_at,
                "updated_at": sample_segment_model.updated_at,
            }
        ]

        schema = ListSegmentPublicSchema(segments=segments_data)

        assert len(schema.segments) == 1
        assert schema.segments[0].name == sample_segment_model.name
