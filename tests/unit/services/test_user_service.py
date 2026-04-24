import pytest
from unittest.mock import AsyncMock, MagicMock
from api.services.users import UserService
from api.schemas.users import UserCreateSchema, UserUpdateSchema
from api.models.users import User
from api.exceptions.users import UserNotFound, UserAlreadyExists
from api.exceptions.companys import CompanyNotFound

@pytest.fixture
def mock_user_repository():
    return MagicMock()

@pytest.fixture
def mock_company_repository():
    return MagicMock()

@pytest.fixture
def user_service(mock_user_repository, mock_company_repository):
    return UserService(mock_user_repository, mock_company_repository)

@pytest.fixture
def sample_user_schema():
    return UserCreateSchema(
        name="Test User",
        email="test@user.com",
        password="password123",
        whatsapp="11999999999",
        profile=1,
        company_id=1
    )

class TestUserService:
    @pytest.mark.asyncio
    async def test_create_user_success(self, user_service, mock_company_repository, mock_user_repository, sample_user_schema):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_user_repository.get_by_email = AsyncMock(return_value=None)
        mock_user = MagicMock(spec=User)
        mock_user_repository.save = AsyncMock(return_value=mock_user)

        result = await user_service.create(sample_user_schema)

        assert result == mock_user
        mock_company_repository.get_by_id.assert_called_once_with(1)
        mock_user_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_user_email_already_exists(self, user_service, mock_company_repository, mock_user_repository, sample_user_schema):
        mock_company_repository.get_by_id = AsyncMock(return_value=MagicMock())
        mock_user_repository.get_by_email = AsyncMock(return_value=MagicMock())

        with pytest.raises(UserAlreadyExists):
            await user_service.create(sample_user_schema)

    @pytest.mark.asyncio
    async def test_get_by_id_and_company_success(self, user_service, mock_user_repository):
        mock_user = MagicMock(spec=User)
        mock_user_repository.get_by_id_and_company = AsyncMock(return_value=mock_user)

        result = await user_service.get_by_id_and_company(1, 1)

        assert result == mock_user

    @pytest.mark.asyncio
    async def test_update_user_success(self, user_service, mock_user_repository):
        existing_user = MagicMock(spec=User)
        existing_user.email = "old@user.com"
        mock_user_repository.get_by_id = AsyncMock(return_value=existing_user)
        mock_user_repository.get_by_email = AsyncMock(return_value=None)
        mock_user_repository.update = AsyncMock(return_value=existing_user)

        update_data = UserUpdateSchema(name="New Name", email="new@user.com")
        result = await user_service.update(1, update_data)

        assert result.name == "New Name"
        mock_user_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_authenticate_success(self, user_service, mock_user_repository):
        from api.security.password import hash_password
        mock_user = MagicMock(spec=User)
        mock_user.password = hash_password("password123")
        mock_user_repository.get_by_email = AsyncMock(return_value=mock_user)

        result = await user_service.authenticate("test@user.com", "password123")

        assert result == mock_user

    @pytest.mark.asyncio
    async def test_authenticate_invalid_password(self, user_service, mock_user_repository):
        from api.security.password import hash_password
        mock_user = MagicMock(spec=User)
        mock_user.password = hash_password("password123")
        mock_user_repository.get_by_email = AsyncMock(return_value=mock_user)

        with pytest.raises(UserNotFound):
            await user_service.authenticate("test@user.com", "wrongpassword")
