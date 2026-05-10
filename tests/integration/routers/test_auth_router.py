import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch, MagicMock
from api.app import app

@pytest.fixture
async def test_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

class TestAuthEndpoints:
    @pytest.mark.asyncio
    async def test_auth_success_sets_cookie_and_returns_user_info(self, test_client: AsyncClient):
        # Mock user
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.password = "hashed_password"
        mock_user.company_id = 1
        mock_user.name = "Test User"

        with patch("api.repositories.users.UserRepository.get_by_email", new_callable=AsyncMock) as mock_get_email, \
             patch("api.routers.auth.verify_password", return_value=True), \
             patch("api.routers.auth.create_access_token", return_value="fake-token"):
            
            mock_get_email.return_value = mock_user
            
            response = await test_client.post(
                "/api/v1/auth/",
                json={"email": "test@example.com", "password": "password123"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "Test User"
            assert data["email"] == "test@example.com"
            assert data["company_id"] == 1
            assert "access_token" not in data
            assert "access_token" in response.cookies
            assert response.cookies["access_token"] == "fake-token"

    @pytest.mark.asyncio
    async def test_logout_clears_cookie(self, test_client: AsyncClient):
        # Set a cookie first
        test_client.cookies.set("access_token", "some-token")
        
        response = await test_client.post("/api/v1/auth/logout")
        
        assert response.status_code == 200
        assert response.json() == {"message": "Logout realizado com sucesso"}
        # In httpx, delete_cookie might just expire it or remove it from the client
        assert "access_token" not in response.cookies or response.cookies.get("access_token") == ""
