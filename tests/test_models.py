"""Unit tests for user models."""

import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch
from app.models.user import User


class TestUserModel:
    """Test cases for User model."""
    
    def test_user_creation(self):
        """Test basic user creation."""
        user_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "hashed_password": "hashed_password_123"
        }
        
        user = User(**user_data)
        
        assert user.name == "John Doe"
        assert user.email == "john.doe@example.com"
        assert user.hashed_password == "hashed_password_123"
        assert user.active is False  # Default value
        assert user.role == "user"  # Default value
        assert user.login_attempts == 0  # Default value
        assert user.locked_until is None  # Default value
    
    def test_user_default_values(self):
        """Test user model default values."""
        user = User(
            name="Test User",
            email="test@example.com",
            hashed_password="hashed_pass"
        )
        
        # Check default values
        assert user.active is False
        assert user.role == "user"
        assert user.login_attempts == 0
        assert user.locked_until is None
        assert user.last_login is None
        assert user.phone is None
        assert user.address is None
        assert user.profile_picture_url is None
        assert user.cover_picture_url is None
        
        # Check that timestamps are set
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)
    
    def test_user_with_optional_fields(self):
        """Test user creation with optional fields."""
        user_data = {
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "hashed_password": "hashed_password_456",
            "active": True,
            "role": "admin",
            "phone": "+1234567890",
            "address": "123 Main St",
            "profile_picture_url": "https://example.com/profile.jpg",
            "cover_picture_url": "https://example.com/cover.jpg",
        }
        
        user = User(**user_data)
        
        assert user.name == "Jane Smith"
        assert user.active is True
        assert user.role == "admin"
        assert user.phone == "+1234567890"
        assert user.address == "123 Main St"
        assert user.profile_picture_url == "https://example.com/profile.jpg"
        assert user.cover_picture_url == "https://example.com/cover.jpg"
    
    @pytest.mark.asyncio
    async def test_save_updates_timestamp(self):
        """Test that save method updates the updated_at timestamp."""
        user = User(
            name="Test User",
            email="test@example.com",
            hashed_password="hashed_pass"
        )
        
        original_updated_at = user.updated_at
        
        # Mock the parent save method
        with patch.object(User.__bases__[0], 'save', new_callable=AsyncMock) as mock_save:
            mock_save.return_value = user
            
            # Wait a bit to ensure timestamp difference
            import asyncio
            await asyncio.sleep(0.001)
            
            result = await user.save()
            
            # Check that updated_at was changed
            assert user.updated_at > original_updated_at
            assert result == user
            mock_save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_find_by_email(self):
        """Test finding user by email."""
        test_email = "test@example.com"
        
        with patch.object(User, 'find_one', new_callable=AsyncMock) as mock_find_one:
            mock_user = User(name="Test", email=test_email, hashed_password="hash")
            mock_find_one.return_value = mock_user
            
            result = await User.find_by_email(test_email)
            
            assert result == mock_user
            mock_find_one.assert_called_once_with({"email": test_email.lower().strip()})
    
    @pytest.mark.asyncio
    async def test_find_by_email_normalizes_input(self):
        """Test that find_by_email normalizes email input."""
        test_email = "  TEST@EXAMPLE.COM  "
        expected_normalized = "test@example.com"
        
        with patch.object(User, 'find_one', new_callable=AsyncMock) as mock_find_one:
            mock_find_one.return_value = None
            
            await User.find_by_email(test_email)
            
            mock_find_one.assert_called_once_with({"email": expected_normalized})
    
    @pytest.mark.asyncio
    async def test_email_exists_true(self):
        """Test email_exists returns True when email exists."""
        test_email = "existing@example.com"
        
        with patch.object(User, 'find_by_email', new_callable=AsyncMock) as mock_find:
            mock_user = User(name="Test", email=test_email, hashed_password="hash")
            mock_find.return_value = mock_user
            
            result = await User.email_exists(test_email)
            
            assert result is True
            mock_find.assert_called_once_with(test_email)
    
    @pytest.mark.asyncio
    async def test_email_exists_false(self):
        """Test email_exists returns False when email doesn't exist."""
        test_email = "nonexistent@example.com"
        
        with patch.object(User, 'find_by_email', new_callable=AsyncMock) as mock_find:
            mock_find.return_value = None
            
            result = await User.email_exists(test_email)
            
            assert result is False
            mock_find.assert_called_once_with(test_email)
    
    @pytest.mark.asyncio
    async def test_find_active_users(self):
        """Test finding active users."""
        with patch.object(User, 'find', new_callable=AsyncMock) as mock_find:
            mock_query = AsyncMock()
            mock_query.limit.return_value.to_list = AsyncMock(return_value=[])
            mock_find.return_value = mock_query
            
            result = await User.find_active_users(limit=50)
            
            assert result == []
            mock_find.assert_called_once_with({"active": True})
            mock_query.limit.assert_called_once_with(50)
    
    @pytest.mark.asyncio
    async def test_activate_user(self):
        """Test activating a user account."""
        user = User(name="Test", email="test@example.com", hashed_password="hash")
        assert user.active is False
        
        with patch.object(user, 'save', new_callable=AsyncMock) as mock_save:
            mock_save.return_value = user
            
            result = await user.activate()
            
            assert user.active is True
            assert result == user
            mock_save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_deactivate_user(self):
        """Test deactivating a user account."""
        user = User(name="Test", email="test@example.com", hashed_password="hash", active=True)
        assert user.active is True
        
        with patch.object(user, 'save', new_callable=AsyncMock) as mock_save:
            mock_save.return_value = user
            
            result = await user.deactivate()
            
            assert user.active is False
            assert result == user
            mock_save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_last_login(self):
        """Test updating last login timestamp."""
        user = User(name="Test", email="test@example.com", hashed_password="hash")
        user.login_attempts = 3
        original_last_login = user.last_login
        
        with patch.object(user, 'save', new_callable=AsyncMock) as mock_save:
            mock_save.return_value = user
            
            result = await user.update_last_login()
            
            assert user.last_login != original_last_login
            assert isinstance(user.last_login, datetime)
            assert user.login_attempts == 0  # Should reset failed attempts
            assert result == user
            mock_save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_increment_login_attempts(self):
        """Test incrementing failed login attempts."""
        user = User(name="Test", email="test@example.com", hashed_password="hash")
        assert user.login_attempts == 0
        
        with patch.object(user, 'save', new_callable=AsyncMock) as mock_save:
            mock_save.return_value = user
            
            result = await user.increment_login_attempts()
            
            assert user.login_attempts == 1
            assert user.locked_until is None  # Not locked yet
            assert result == user
            mock_save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_increment_login_attempts_locks_account(self):
        """Test that account gets locked after 5 failed attempts."""
        user = User(name="Test", email="test@example.com", hashed_password="hash")
        user.login_attempts = 4  # One away from lock
        
        with patch.object(user, 'save', new_callable=AsyncMock) as mock_save:
            mock_save.return_value = user
            
            result = await user.increment_login_attempts()
            
            assert user.login_attempts == 5
            assert user.locked_until is not None
            assert isinstance(user.locked_until, datetime)
            assert result == user
            mock_save.assert_called_once()
    
    def test_is_locked_false_when_no_lock(self):
        """Test is_locked returns False when no lock is set."""
        user = User(name="Test", email="test@example.com", hashed_password="hash")
        assert user.locked_until is None
        assert user.is_locked() is False
    
    def test_is_locked_false_when_lock_expired(self):
        """Test is_locked returns False when lock has expired."""
        user = User(name="Test", email="test@example.com", hashed_password="hash")
        # Set lock to past time
        past_time = datetime.now(timezone.utc).replace(minute=datetime.now(timezone.utc).minute - 1)
        user.locked_until = past_time
        
        assert user.is_locked() is False
    
    def test_is_locked_true_when_locked(self):
        """Test is_locked returns True when account is currently locked."""
        user = User(name="Test", email="test@example.com", hashed_password="hash")
        # Set lock to future time
        future_time = datetime.now(timezone.utc).replace(minute=datetime.now(timezone.utc).minute + 30)
        user.locked_until = future_time
        
        assert user.is_locked() is True
    
    @pytest.mark.asyncio
    async def test_unlock_account(self):
        """Test unlocking a user account."""
        user = User(name="Test", email="test@example.com", hashed_password="hash")
        user.locked_until = datetime.now(timezone.utc).replace(minute=datetime.now(timezone.utc).minute + 30)
        user.login_attempts = 5
        
        with patch.object(user, 'save', new_callable=AsyncMock) as mock_save:
            mock_save.return_value = user
            
            result = await user.unlock_account()
            
            assert user.locked_until is None
            assert user.login_attempts == 0
            assert result == user
            mock_save.assert_called_once()
    
    def test_to_dict_excludes_sensitive_by_default(self):
        """Test to_dict excludes sensitive information by default."""
        user = User(
            name="Test User",
            email="test@example.com",
            hashed_password="secret_hash",
            login_attempts=3,
            locked_until=datetime.now(timezone.utc)
        )
        
        with patch.object(user, 'dict') as mock_dict:
            mock_dict.return_value = {
                'id': 'test_id',
                'name': 'Test User',
                'email': 'test@example.com',
                'hashed_password': 'secret_hash',
                'login_attempts': 3,
                'locked_until': datetime.now(timezone.utc),
                'active': False
            }
            
            result = user.to_dict()
            
            assert 'hashed_password' not in result
            assert 'login_attempts' not in result
            assert 'locked_until' not in result
            assert result['id'] == 'test_id'
            assert result['name'] == 'Test User'
            assert result['email'] == 'test@example.com'
            assert result['active'] is False
    
    def test_to_dict_includes_sensitive_when_requested(self):
        """Test to_dict includes sensitive information when requested."""
        user = User(
            name="Test User",
            email="test@example.com",
            hashed_password="secret_hash",
            login_attempts=3
        )
        
        with patch.object(user, 'dict') as mock_dict:
            mock_dict.return_value = {
                'id': 'test_id',
                'name': 'Test User',
                'email': 'test@example.com',
                'hashed_password': 'secret_hash',
                'login_attempts': 3,
                'active': False
            }
            
            result = user.to_dict(exclude_sensitive=False)
            
            assert 'hashed_password' in result
            assert 'login_attempts' in result
            assert result['hashed_password'] == 'secret_hash'
            assert result['login_attempts'] == 3


class TestUserModelIntegration:
    """Integration tests for User model."""
    
    def test_user_lifecycle(self):
        """Test complete user lifecycle."""
        # Create user
        user = User(
            name="Lifecycle Test",
            email="lifecycle@example.com",
            hashed_password="hashed_pass"
        )
        
        # Check initial state
        assert user.active is False
        assert user.login_attempts == 0
        assert user.locked_until is None
        
        # Test account locking simulation
        for i in range(5):
            user.login_attempts += 1
        
        if user.login_attempts >= 5:
            user.locked_until = datetime.now(timezone.utc).replace(
                minute=datetime.now(timezone.utc).minute + 30
            )
        
        assert user.is_locked() is True
        
        # Test unlocking
        user.locked_until = None
        user.login_attempts = 0
        assert user.is_locked() is False
    
    def test_user_data_integrity(self):
        """Test user data integrity and validation."""
        # Test with minimal required data
        user = User(
            name="Minimal User",
            email="minimal@example.com",
            hashed_password="hash"
        )
        
        assert user.name == "Minimal User"
        assert user.email == "minimal@example.com"
        assert user.hashed_password == "hash"
        
        # Test with maximum data
        full_user = User(
            name="Full User",
            email="full@example.com",
            hashed_password="full_hash",
            active=True,
            role="admin",
            phone="+1234567890",
            address="123 Full St",
            profile_picture_url="https://example.com/profile.jpg",
            cover_picture_url="https://example.com/cover.jpg"
        )
        
        assert full_user.role == "admin"
        assert full_user.phone == "+1234567890"
        assert full_user.address == "123 Full St"
