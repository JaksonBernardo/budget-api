import pytest
from unittest.mock import AsyncMock, MagicMock
from typing import AsyncGenerator
from httpx import AsyncClient

from api.app import app
from api.core.settings import Settings


class TestSettings(Settings):
    """Configurações de teste que sobrescrevem as configurações reais"""
    
    class Config:
        arbitrary_types_allowed = True
    
    DB_HOST: str = "127.0.0.1"
    DB_USER: str = "test_user"
    DB_PASSWORD: str = "test_password"
    DB_PORT: int = 3306
    DB_NAME: str = "test_db"
    DATABASE_URL: str = "mysql+aiomysql://test_user:test_password@127.0.0.1:3306/test_db"
    JWT_SECRET_KEY: str = "test_secret_key_for_testing_purposes_only"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60
    URL_CORS: str = "http://test.local"


@pytest.fixture(scope="session")
def anyio_backend():
    """Configura o backend para testes async"""
    return "asyncio"


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Cria um cliente HTTP assíncrono para testes de integração"""
    async with AsyncClient(transport=None, base_url="http://test") as ac:
        ac.app = app
        yield ac


@pytest.fixture
def mock_db_session() -> MagicMock:
    """Cria um mock da sessão do banco de dados"""
    session = MagicMock()
    session.add = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    session.execute = AsyncMock()
    session.scalars = MagicMock()
    session.scalars.return_value = MagicMock()
    session.scalars.return_value.all = AsyncMock(return_value=[])
    session.scalars.return_value.one = AsyncMock()
    session.scalar_one_or_none = AsyncMock()
    return session


@pytest.fixture
def mock_segment_repository() -> MagicMock:
    """Cria um mock do repositório de segmentos"""
    repo = MagicMock()
    repo.save = AsyncMock()
    repo.get_by_company_id = AsyncMock(return_value=[])
    repo.get_by_id = AsyncMock()
    repo.delete_by_id = AsyncMock()
    repo.update = AsyncMock()
    return repo


@pytest.fixture
def mock_company_repository() -> MagicMock:
    """Cria um mock do repositório de empresas"""
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    return repo


@pytest.fixture
def sample_segment_data() -> dict:
    """Dados de exemplo para testes de segmento"""
    return {
        "name": "Segmento Teste",
        "contract": "Contrato de teste",
        "company_id": 1,
    }


@pytest.fixture
def sample_segment_model(sample_segment_data) -> MagicMock:
    """Cria um mock de modelo Segment"""
    segment = MagicMock()
    segment.id = 1
    segment.name = sample_segment_data["name"]
    segment.contract = sample_segment_data["contract"]
    segment.company_id = sample_segment_data["company_id"]
    segment.created_at = "2024-01-01T00:00:00"
    segment.updated_at = "2024-01-01T00:00:00"
    return segment


@pytest.fixture
def sample_company_data() -> dict:
    """Dados de exemplo para testes de empresa"""
    return {
        "id": 1,
        "name": "Empresa Teste LTDA",
        "document": "12.345.678/0001-90",
    }


@pytest.fixture
def sample_company_model(sample_company_data) -> MagicMock:
    """Cria um mock de modelo Company"""
    company = MagicMock()
    company.id = sample_company_data["id"]
    company.name = sample_company_data["name"]
    company.document = sample_company_data["document"]
    return company
