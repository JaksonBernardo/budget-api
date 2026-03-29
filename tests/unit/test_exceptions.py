"""Testes para exceptions"""
import pytest

from api.exceptions.segments import (
    SegmentInvalidName,
    SegmentNotFound,
    SegmentAccesDenied,
)
from api.exceptions.companys import (
    CompanyNotFound,
    InvalidTypeCompanyId,
    ZeroCompanyId,
)
from api.exceptions.map_exceptions import map_exception


class TestSegmentExceptions:
    """Testes para exceptions de segmentos"""

    def test_segment_invalid_name_default_message(self):
        """Testa exceção de nome inválido com mensagem padrão"""
        exc = SegmentInvalidName()
        assert str(exc) == "Nome do segmento não pode ser inválido ou vazio"

    def test_segment_invalid_name_custom_message(self):
        """Testa exceção de nome inválido com mensagem customizada"""
        custom_message = "Mensagem customizada"
        exc = SegmentInvalidName(custom_message)
        assert str(exc) == custom_message

    def test_segment_not_found(self):
        """Testa exceção de segmento não encontrado"""
        exc = SegmentNotFound()
        assert str(exc) == "Segmento não encontrado"
        assert exc.status_code == 404

    def test_segment_access_denied(self):
        """Testa exceção de acesso negado"""
        exc = SegmentAccesDenied()
        assert str(exc) == "Operação não permitida"
        assert exc.status_code == 403


class TestCompanyExceptions:
    """Testes para exceptions de empresas"""

    def test_company_not_found(self):
        """Testa exceção de empresa não encontrada"""
        exc = CompanyNotFound()
        assert str(exc) == "Company não encontrada"
        assert exc.status_code == 404

    def test_invalid_type_company_id(self):
        """Testa exceção de tipo inválido de company_id"""
        exc = InvalidTypeCompanyId()
        assert str(exc) == "ID Company deve ser do tipo inteiro"

    def test_zero_company_id(self):
        """Testa exceção de company_id zero"""
        exc = ZeroCompanyId()
        assert str(exc) == "ID Company não pode ser menor ou igual a zero"


class TestMapExceptions:
    """Testes para mapeamento de exceptions"""

    def test_map_segment_not_found(self):
        """Testa mapeamento de SegmentNotFound para HTTPException"""
        from fastapi import HTTPException
        
        exc = SegmentNotFound()
        http_exc = map_exception(exc)
        
        assert isinstance(http_exc, HTTPException)
        assert http_exc.status_code == 404

    def test_map_segment_access_denied(self):
        """Testa mapeamento de SegmentAccesDenied para HTTPException"""
        from fastapi import HTTPException
        
        exc = SegmentAccesDenied()
        http_exc = map_exception(exc)
        
        assert isinstance(http_exc, HTTPException)
        assert http_exc.status_code == 403

    def test_map_company_not_found(self):
        """Testa mapeamento de CompanyNotFound para HTTPException"""
        from fastapi import HTTPException
        
        exc = CompanyNotFound()
        http_exc = map_exception(exc)
        
        assert isinstance(http_exc, HTTPException)
        assert http_exc.status_code == 404

    def test_map_segment_invalid_name(self):
        """Testa mapeamento de SegmentInvalidName para HTTPException"""
        from fastapi import HTTPException
        
        exc = SegmentInvalidName()
        http_exc = map_exception(exc)
        
        assert isinstance(http_exc, HTTPException)
        assert http_exc.status_code == 400
