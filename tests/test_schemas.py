"""Unit tests for user schemas."""

import pytest
from pydantic import ValidationError
from app.schemas.user import UserRegisterRequest, UserResponse, UserLoginRequest


class TestUserRegisterRequest:
    """Test cases for UserRegisterRequest schema."""
    
    def test_valid_registration_data(self):
        """Test valid user registration data."""
        valid_data = {
            "username": "john_doe",
            "email": "john.doe@example.com",
            "password": "SecurePass123!"
        }
        
        request = UserRegisterRequest(**valid_data)
        assert request.username == "john_doe"
        assert request.email == "john.doe@example.com"
        assert request.password == "SecurePass123!"
    
    def test_email_validation(self):
        """Test email validation in registration request."""
        # Valid email should work
        valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "ValidPass123!"
        }
        request = UserRegisterRequest(**valid_data)
        assert request.email == "test@example.com"
        
        # Invalid email should fail
        invalid_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "ValidPass123!"
        }
        with pytest.raises(ValidationError) as exc_info:
            UserRegisterRequest(**invalid_data)
        
        errors = exc_info.value.errors()
        assert any("email" in error["loc"] for error in errors)
    
    def test_password_validation(self):
        """Test password validation in registration request."""
        base_data = {
            "username": "testuser",
            "email": "test@example.com"
        }
        
        # Valid password should work
        valid_data = {**base_data, "password": "SecurePass123!"}
        request = UserRegisterRequest(**valid_data)
        assert request.password == "SecurePass123!"
        
        # Weak password should fail
        weak_passwords = [
            "weak",  # Too short
            "password123",  # No uppercase, no special char
            "PASSWORD123!",  # No lowercase
            "Password!",  # No number
            "Password123",  # No special char
        ]
        
        for weak_password in weak_passwords:
            invalid_data = {**base_data, "password": weak_password}
            with pytest.raises(ValidationError) as exc_info:
                UserRegisterRequest(**invalid_data)
            
            errors = exc_info.value.errors()
            assert any("password" in error["loc"] for error in errors)
    
    def test_username_validation(self):
        """Test username validation in registration request."""
        base_data = {
            "email": "test@example.com",
            "password": "ValidPass123!"
        }
        
        # Valid username should work
        valid_data = {**base_data, "username": "valid_user"}
        request = UserRegisterRequest(**valid_data)
        assert request.username == "valid_user"
        
        # Invalid usernames should fail
        invalid_usernames = [
            "ab",  # Too short
            "_invalid",  # Starts with underscore
            "invalid_",  # Ends with underscore
            "invalid@user",  # Invalid character
            "user name",  # Space
        ]
        
        for invalid_username in invalid_usernames:
            invalid_data = {**base_data, "username": invalid_username}
            with pytest.raises(ValidationError) as exc_info:
                UserRegisterRequest(**invalid_data)
            
            errors = exc_info.value.errors()
            assert any("username" in error["loc"] for error in errors)
    
    def test_missing_required_fields(self):
        """Test validation with missing required fields."""
        # Missing username
        with pytest.raises(ValidationError) as exc_info:
            UserRegisterRequest(email="test@example.com", password="ValidPass123!")
        assert any("username" in error["loc"] for error in exc_info.value.errors())
        
        # Missing email
        with pytest.raises(ValidationError) as exc_info:
            UserRegisterRequest(username="testuser", password="ValidPass123!")
        assert any("email" in error["loc"] for error in exc_info.value.errors())
        
        # Missing password
        with pytest.raises(ValidationError) as exc_info:
            UserRegisterRequest(username="testuser", email="test@example.com")
        assert any("password" in error["loc"] for error in exc_info.value.errors())


class TestUserLoginRequest:
    """Test cases for UserLoginRequest schema."""
    
    def test_valid_login_data(self):
        """Test valid user login data."""
        valid_data = {
            "email": "john.doe@example.com",
            "password": "SecurePass123!"
        }
        
        request = UserLoginRequest(**valid_data)
        assert request.email == "john.doe@example.com"
        assert request.password == "SecurePass123!"
    
    def test_email_validation(self):
        """Test email validation in login request."""
        # Valid email should work
        valid_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        request = UserLoginRequest(**valid_data)
        assert request.email == "test@example.com"
        
        # Invalid email should fail
        invalid_data = {
            "email": "invalid-email",
            "password": "password123"
        }
        with pytest.raises(ValidationError) as exc_info:
            UserLoginRequest(**invalid_data)
        
        errors = exc_info.value.errors()
        assert any("email" in error["loc"] for error in errors)
    
    def test_missing_required_fields(self):
        """Test validation with missing required fields."""
        # Missing email
        with pytest.raises(ValidationError) as exc_info:
            UserLoginRequest(password="password123")
        assert any("email" in error["loc"] for error in exc_info.value.errors())
        
        # Missing password
        with pytest.raises(ValidationError) as exc_info:
            UserLoginRequest(email="test@example.com")
        assert any("password" in error["loc"] for error in exc_info.value.errors())


class TestUserResponse:
    """Test cases for UserResponse schema."""
    
    def test_valid_user_response(self):
        """Test valid user response data."""
        valid_data = {
            "id": "507f1f77bcf86cd799439011",
            "username": "john_doe",
            "email": "john.doe@example.com",
            "active": True,
            "role": "user",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
        }
        
        response = UserResponse(**valid_data)
        assert response.id == "507f1f77bcf86cd799439011"
        assert response.username == "john_doe"
        assert response.email == "john.doe@example.com"
        assert response.active is True
        assert response.role == "user"
    
    def test_optional_fields(self):
        """Test optional fields in user response."""
        minimal_data = {
            "id": "507f1f77bcf86cd799439011",
            "username": "john_doe",
            "email": "john.doe@example.com",
            "active": True,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
        }
        
        response = UserResponse(**minimal_data)
        assert response.phone is None
        assert response.address is None
        assert response.profile_picture_url is None
        assert response.cover_picture_url is None
        assert response.role == "user"  # Default value
    
    def test_with_optional_fields(self):
        """Test user response with optional fields populated."""
        full_data = {
            "id": "507f1f77bcf86cd799439011",
            "username": "john_doe",
            "email": "john.doe@example.com",
            "active": True,
            "role": "admin",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "phone": "+1234567890",
            "address": "123 Main St, City, State",
            "profile_picture_url": "https://example.com/profile.jpg",
            "cover_picture_url": "https://example.com/cover.jpg",
        }
        
        response = UserResponse(**full_data)
        assert response.phone == "+1234567890"
        assert response.address == "123 Main St, City, State"
        assert response.profile_picture_url == "https://example.com/profile.jpg"
        assert response.cover_picture_url == "https://example.com/cover.jpg"
        assert response.role == "admin"
    
    def test_missing_required_fields(self):
        """Test validation with missing required fields."""
        required_fields = ["id", "username", "email", "active", "created_at", "updated_at"]
        
        base_data = {
            "id": "507f1f77bcf86cd799439011",
            "username": "john_doe",
            "email": "john.doe@example.com",
            "active": True,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
        }
        
        for field in required_fields:
            incomplete_data = {k: v for k, v in base_data.items() if k != field}
            with pytest.raises(ValidationError) as exc_info:
                UserResponse(**incomplete_data)
            
            errors = exc_info.value.errors()
            assert any(field in error["loc"] for error in errors)


class TestSchemaIntegration:
    """Integration tests for schemas."""
    
    def test_registration_to_response_flow(self):
        """Test the flow from registration request to user response."""
        # Create a registration request
        registration_data = {
            "username": "new_user",
            "email": "new.user@example.com",
            "password": "NewUserPass123!"
        }
        
        registration_request = UserRegisterRequest(**registration_data)
        
        # Simulate creating a user response from registration data
        response_data = {
            "id": "507f1f77bcf86cd799439011",
            "username": registration_request.username,
            "email": registration_request.email,
            "active": False,  # New users start inactive
            "role": "user",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
        }
        
        user_response = UserResponse(**response_data)
        
        assert user_response.username == registration_request.username
        assert user_response.email == registration_request.email
        assert user_response.active is False
        assert user_response.role == "user"
    
    def test_login_request_validation(self):
        """Test login request validation with various inputs."""
        # Test with normalized email
        login_data = {
            "email": "  TEST@EXAMPLE.COM  ",
            "password": "password123"
        }
        
        login_request = UserLoginRequest(**login_data)
        assert login_request.email == "test@example.com"  # Should be normalized
    
    def test_schema_examples(self):
        """Test that schema examples are valid."""
        # Test UserRegisterRequest example
        register_example = {
            "username": "john_doe",
            "email": "john.doe@example.com",
            "password": "SecurePass123!"
        }
        
        register_request = UserRegisterRequest(**register_example)
        assert register_request.username == "john_doe"
        
        # Test UserLoginRequest example
        login_example = {
            "email": "john.doe@example.com",
            "password": "SecurePass123!"
        }
        
        login_request = UserLoginRequest(**login_example)
        assert login_request.email == "john.doe@example.com"
        
        # Test UserResponse example
        response_example = {
            "id": "507f1f77bcf86cd799439011",
            "username": "john_doe",
            "email": "john.doe@example.com",
            "active": True,
            "role": "user",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "phone": None,
            "address": None,
            "profile_picture_url": None,
            "cover_picture_url": None
        }
        
        user_response = UserResponse(**response_example)
        assert user_response.id == "507f1f77bcf86cd799439011"
