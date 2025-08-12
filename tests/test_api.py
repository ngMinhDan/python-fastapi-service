"""Unit tests for user API endpoints."""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException, status
from app.api.v1.user import register_user, login_user
from app.schemas.user import UserRegisterRequest, UserLoginRequest
from app.models.user import User


class TestUserRegistrationAPI:
    """Test cases for user registration endpoint."""
    
    @pytest.mark.asyncio
    async def test_successful_registration(self):
        """Test successful user registration."""
        request_data = UserRegisterRequest(
            username="newuser",
            email="newuser@example.com",
            password="SecurePass123!"
        )
        
        # Mock dependencies
        with patch('app.api.v1.user.User.email_exists', new_callable=AsyncMock) as mock_email_exists, \
             patch('app.api.v1.user.get_password_hash') as mock_hash, \
             patch('app.api.v1.user.create_access_token') as mock_token:
            
            # Setup mocks
            mock_email_exists.return_value = False
            mock_hash.return_value = "hashed_password"
            mock_token.return_value = "jwt_token_123"
            
            # Mock user creation and save
            mock_user = User(
                name="newuser",
                email="newuser@example.com",
                hashed_password="hashed_password"
            )
            mock_user.id = "user_id_123"
            
            with patch('app.api.v1.user.User') as mock_user_class:
                mock_user_instance = AsyncMock()
                mock_user_instance.id = "user_id_123"
                mock_user_instance.name = "newuser"
                mock_user_instance.email = "newuser@example.com"
                mock_user_instance.active = False
                mock_user_instance.role = "user"
                mock_user_instance.save = AsyncMock(return_value=mock_user_instance)
                mock_user_class.return_value = mock_user_instance
                
                # Call the endpoint
                response = await register_user(request_data)
                
                # Assertions
                assert response.access_token == "jwt_token_123"
                assert response.token_type == "bearer"
                
                # Verify mocks were called correctly
                mock_email_exists.assert_called_once_with("newuser@example.com")
                mock_hash.assert_called_once_with("SecurePass123!")
                mock_user_class.assert_called_once()
                mock_user_instance.save.assert_called_once()
                mock_token.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_registration_email_already_exists(self):
        """Test registration with existing email."""
        request_data = UserRegisterRequest(
            username="existinguser",
            email="existing@example.com",
            password="SecurePass123!"
        )
        
        with patch('app.api.v1.user.User.email_exists', new_callable=AsyncMock) as mock_email_exists:
            mock_email_exists.return_value = True
            
            with pytest.raises(HTTPException) as exc_info:
                await register_user(request_data)
            
            assert exc_info.value.status_code == status.HTTP_409_CONFLICT
            assert "Email address already registered" in exc_info.value.detail
            mock_email_exists.assert_called_once_with("existing@example.com")
    
    @pytest.mark.asyncio
    async def test_registration_database_error(self):
        """Test registration with database error."""
        request_data = UserRegisterRequest(
            username="testuser",
            email="test@example.com",
            password="SecurePass123!"
        )
        
        with patch('app.api.v1.user.User.email_exists', new_callable=AsyncMock) as mock_email_exists, \
             patch('app.api.v1.user.get_password_hash') as mock_hash:
            
            mock_email_exists.return_value = False
            mock_hash.return_value = "hashed_password"
            
            with patch('app.api.v1.user.User') as mock_user_class:
                mock_user_instance = AsyncMock()
                mock_user_instance.save = AsyncMock(side_effect=Exception("Database error"))
                mock_user_class.return_value = mock_user_instance
                
                with pytest.raises(HTTPException) as exc_info:
                    await register_user(request_data)
                
                assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
                assert "Internal server error during registration" in exc_info.value.detail


class TestUserLoginAPI:
    """Test cases for user login endpoint."""
    
    @pytest.mark.asyncio
    async def test_successful_login(self):
        """Test successful user login."""
        request_data = UserLoginRequest(
            email="user@example.com",
            password="UserPass123!"
        )
        
        # Mock user
        mock_user = AsyncMock()
        mock_user.id = "user_id_123"
        mock_user.name = "Test User"
        mock_user.email = "user@example.com"
        mock_user.active = True
        mock_user.role = "user"
        mock_user.hashed_password = "hashed_password"
        mock_user.is_locked.return_value = False
        mock_user.update_last_login = AsyncMock(return_value=mock_user)
        
        with patch('app.api.v1.user.User.find_by_email', new_callable=AsyncMock) as mock_find, \
             patch('app.api.v1.user.verify_password') as mock_verify, \
             patch('app.api.v1.user.create_access_token') as mock_token:
            
            # Setup mocks
            mock_find.return_value = mock_user
            mock_verify.return_value = True
            mock_token.return_value = "jwt_token_456"
            
            # Call the endpoint
            response = await login_user(request_data)
            
            # Assertions
            assert response.access_token == "jwt_token_456"
            assert response.token_type == "bearer"
            
            # Verify mocks were called correctly
            mock_find.assert_called_once_with("user@example.com")
            mock_verify.assert_called_once_with("UserPass123!", "hashed_password")
            mock_user.update_last_login.assert_called_once()
            mock_token.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_login_user_not_found(self):
        """Test login with non-existent user."""
        request_data = UserLoginRequest(
            email="nonexistent@example.com",
            password="Password123!"
        )
        
        with patch('app.api.v1.user.User.find_by_email', new_callable=AsyncMock) as mock_find:
            mock_find.return_value = None
            
            with pytest.raises(HTTPException) as exc_info:
                await login_user(request_data)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert "Invalid email or password" in exc_info.value.detail
            mock_find.assert_called_once_with("nonexistent@example.com")
    
    @pytest.mark.asyncio
    async def test_login_account_locked(self):
        """Test login with locked account."""
        request_data = UserLoginRequest(
            email="locked@example.com",
            password="Password123!"
        )
        
        mock_user = AsyncMock()
        mock_user.is_locked.return_value = True
        
        with patch('app.api.v1.user.User.find_by_email', new_callable=AsyncMock) as mock_find:
            mock_find.return_value = mock_user
            
            with pytest.raises(HTTPException) as exc_info:
                await login_user(request_data)
            
            assert exc_info.value.status_code == status.HTTP_423_LOCKED
            assert "Account is temporarily locked" in exc_info.value.detail
            mock_find.assert_called_once_with("locked@example.com")
            mock_user.is_locked.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_login_invalid_password(self):
        """Test login with invalid password."""
        request_data = UserLoginRequest(
            email="user@example.com",
            password="WrongPassword123!"
        )
        
        mock_user = AsyncMock()
        mock_user.hashed_password = "hashed_password"
        mock_user.is_locked.return_value = False
        mock_user.increment_login_attempts = AsyncMock(return_value=mock_user)
        
        with patch('app.api.v1.user.User.find_by_email', new_callable=AsyncMock) as mock_find, \
             patch('app.api.v1.user.verify_password') as mock_verify:
            
            mock_find.return_value = mock_user
            mock_verify.return_value = False
            
            with pytest.raises(HTTPException) as exc_info:
                await login_user(request_data)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert "Invalid email or password" in exc_info.value.detail
            
            mock_find.assert_called_once_with("user@example.com")
            mock_verify.assert_called_once_with("WrongPassword123!", "hashed_password")
            mock_user.increment_login_attempts.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_login_database_error(self):
        """Test login with database error."""
        request_data = UserLoginRequest(
            email="user@example.com",
            password="Password123!"
        )
        
        with patch('app.api.v1.user.User.find_by_email', new_callable=AsyncMock) as mock_find:
            mock_find.side_effect = Exception("Database connection error")
            
            with pytest.raises(HTTPException) as exc_info:
                await login_user(request_data)
            
            assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Internal server error during login" in exc_info.value.detail


class TestAPIIntegration:
    """Integration tests for API endpoints."""
    
    @pytest.mark.asyncio
    async def test_registration_login_flow(self):
        """Test complete registration and login flow."""
        # Registration data
        register_data = UserRegisterRequest(
            username="flowtest",
            email="flowtest@example.com",
            password="FlowTest123!"
        )
        
        # Mock successful registration
        with patch('app.api.v1.user.User.email_exists', new_callable=AsyncMock) as mock_email_exists, \
             patch('app.api.v1.user.get_password_hash') as mock_hash, \
             patch('app.api.v1.user.create_access_token') as mock_token:
            
            mock_email_exists.return_value = False
            mock_hash.return_value = "hashed_flowtest_password"
            mock_token.return_value = "registration_token"
            
            mock_user = AsyncMock()
            mock_user.id = "flowtest_user_id"
            mock_user.name = "flowtest"
            mock_user.email = "flowtest@example.com"
            mock_user.active = False
            mock_user.role = "user"
            mock_user.save = AsyncMock(return_value=mock_user)
            
            with patch('app.api.v1.user.User') as mock_user_class:
                mock_user_class.return_value = mock_user
                
                # Register user
                register_response = await register_user(register_data)
                assert register_response.access_token == "registration_token"
        
        # Login data
        login_data = UserLoginRequest(
            email="flowtest@example.com",
            password="FlowTest123!"
        )
        
        # Mock successful login
        mock_login_user = AsyncMock()
        mock_login_user.id = "flowtest_user_id"
        mock_login_user.email = "flowtest@example.com"
        mock_login_user.hashed_password = "hashed_flowtest_password"
        mock_login_user.is_locked.return_value = False
        mock_login_user.update_last_login = AsyncMock(return_value=mock_login_user)
        
        with patch('app.api.v1.user.User.find_by_email', new_callable=AsyncMock) as mock_find, \
             patch('app.api.v1.user.verify_password') as mock_verify, \
             patch('app.api.v1.user.create_access_token') as mock_login_token:
            
            mock_find.return_value = mock_login_user
            mock_verify.return_value = True
            mock_login_token.return_value = "login_token"
            
            # Login user
            login_response = await login_user(login_data)
            assert login_response.access_token == "login_token"
    
    def test_api_error_handling(self):
        """Test API error handling consistency."""
        # Test that all endpoints use proper HTTP status codes
        # and consistent error message formats
        
        # This would be expanded in a real application to test
        # error handling patterns across all endpoints
        pass
    
    def test_api_response_schemas(self):
        """Test that API responses match expected schemas."""
        # Test that response models are properly structured
        # and contain all required fields
        
        # This would be expanded to validate response schemas
        # against OpenAPI specifications
        pass


class TestAPIValidation:
    """Test API input validation."""
    
    def test_registration_request_validation(self):
        """Test registration request validation."""
        # Valid request should work
        valid_data = {
            "username": "validuser",
            "email": "valid@example.com",
            "password": "ValidPass123!"
        }
        request = UserRegisterRequest(**valid_data)
        assert request.username == "validuser"
        
        # Invalid requests should fail
        invalid_cases = [
            {"username": "ab", "email": "valid@example.com", "password": "ValidPass123!"},  # Username too short
            {"username": "validuser", "email": "invalid-email", "password": "ValidPass123!"},  # Invalid email
            {"username": "validuser", "email": "valid@example.com", "password": "weak"},  # Weak password
        ]
        
        for invalid_data in invalid_cases:
            with pytest.raises(Exception):  # Could be ValidationError or ValueError
                UserRegisterRequest(**invalid_data)
    
    def test_login_request_validation(self):
        """Test login request validation."""
        # Valid request should work
        valid_data = {
            "email": "user@example.com",
            "password": "password123"
        }
        request = UserLoginRequest(**valid_data)
        assert request.email == "user@example.com"
        
        # Invalid email should fail
        with pytest.raises(Exception):
            UserLoginRequest(email="invalid-email", password="password123")


# Fixtures for testing
@pytest.fixture
def mock_user():
    """Create a mock user for testing."""
    user = AsyncMock()
    user.id = "test_user_id"
    user.name = "Test User"
    user.email = "test@example.com"
    user.active = True
    user.role = "user"
    user.hashed_password = "hashed_password"
    user.is_locked.return_value = False
    return user


@pytest.fixture
def valid_registration_data():
    """Valid registration data for testing."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123!"
    }


@pytest.fixture
def valid_login_data():
    """Valid login data for testing."""
    return {
        "email": "test@example.com",
        "password": "TestPass123!"
    }
