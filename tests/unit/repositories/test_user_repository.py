import pytest
from unittest.mock import AsyncMock, MagicMock
from api.repositories.users import UserRepository
from api.models.users import User

class TestUserRepository:
    @pytest.mark.asyncio
    async def test_save_user_success(self, mock_db_session):
        mock_user = MagicMock(spec=User)
        repository = UserRepository(mock_db_session)
        
        result = await repository.save(mock_user)
        
        mock_db_session.add.assert_called_once_with(mock_user)
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_user)
        assert result == mock_user

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, mock_db_session):
        mock_user = MagicMock(spec=User)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = UserRepository(mock_db_session)
        
        result = await repository.get_by_id(1)
        
        assert result == mock_user

    @pytest.mark.asyncio
    async def test_get_by_email_success(self, mock_db_session):
        mock_user = MagicMock(spec=User)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = UserRepository(mock_db_session)
        
        result = await repository.get_by_email("test@user.com")
        
        assert result == mock_user

    @pytest.mark.asyncio
    async def test_update_success(self, mock_db_session):
        mock_user = MagicMock(spec=User)
        mock_db_session.merge = AsyncMock()
        repository = UserRepository(mock_db_session)
        
        result = await repository.update(mock_user)
        
        mock_db_session.merge.assert_called_once_with(mock_user)
        mock_db_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, mock_db_session):
        mock_user = MagicMock(spec=User)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        repository = UserRepository(mock_db_session)
        
        result = await repository.delete_by_id(1)
        
        assert result is True
        mock_db_session.commit.assert_called_once()
