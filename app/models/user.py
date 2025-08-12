"""User model for MongoDB using Beanie ODM."""

from typing import Optional, List
from datetime import datetime, timezone
from beanie import Document, Indexed
from pydantic import Field
from pymongo import IndexModel, ASCENDING


class User(Document):
    """User document model for MongoDB.
    
    This model represents a user in the system with all necessary
    fields for authentication, profile information, and metadata.
    """
    
    # Core user fields
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: Indexed(str, unique=True) = Field(..., description="Unique email address")
    hashed_password: str = Field(..., description="Hashed password")
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Account status and role
    active: bool = Field(default=False, description="Account activation status")
    role: str = Field(default="user", description="User role")
    
    # Optional profile fields
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    address: Optional[str] = Field(None, max_length=500, description="Address")
    profile_picture_url: Optional[str] = Field(None, description="Profile picture URL")
    cover_picture_url: Optional[str] = Field(None, description="Cover picture URL")
    
    # Account metadata
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    login_attempts: int = Field(default=0, description="Failed login attempts")
    locked_until: Optional[datetime] = Field(None, description="Account lock expiry")
    
    class Settings:
        """Beanie document settings."""
        name = "users"
        indexes = [
            IndexModel([("email", ASCENDING)], unique=True),
            IndexModel([("active", ASCENDING)]),
            IndexModel([("role", ASCENDING)]),
            IndexModel([("created_at", ASCENDING)]),
        ]
    
    async def save(self, *args, **kwargs) -> "User":
        """Override save method to update timestamp.
        
        Returns:
            User: The saved user document
        """
        self.updated_at = datetime.now(timezone.utc)
        return await super().save(*args, **kwargs)
    
    @classmethod
    async def find_by_email(cls, email: str) -> Optional["User"]:
        """Find user by email address.
        
        Args:
            email: Email address to search for
            
        Returns:
            Optional[User]: User document if found, None otherwise
        """
        return await cls.find_one({"email": email.lower().strip()})
    
    @classmethod
    async def email_exists(cls, email: str) -> bool:
        """Check if email address already exists.
        
        Args:
            email: Email address to check
            
        Returns:
            bool: True if email exists, False otherwise
        """
        user = await cls.find_by_email(email)
        return user is not None
    
    @classmethod
    async def find_active_users(cls, limit: int = 100) -> List["User"]:
        """Find active users.
        
        Args:
            limit: Maximum number of users to return
            
        Returns:
            List[User]: List of active users
        """
        return await cls.find({"active": True}).limit(limit).to_list()
    
    async def activate(self) -> "User":
        """Activate user account.
        
        Returns:
            User: The updated user document
        """
        self.active = True
        return await self.save()
    
    async def deactivate(self) -> "User":
        """Deactivate user account.
        
        Returns:
            User: The updated user document
        """
        self.active = False
        return await self.save()
    
    async def update_last_login(self) -> "User":
        """Update last login timestamp.
        
        Returns:
            User: The updated user document
        """
        self.last_login = datetime.now(timezone.utc)
        self.login_attempts = 0  # Reset failed attempts on successful login
        return await self.save()
    
    async def increment_login_attempts(self) -> "User":
        """Increment failed login attempts.
        
        Returns:
            User: The updated user document
        """
        self.login_attempts += 1
        
        # Lock account after 5 failed attempts for 30 minutes
        if self.login_attempts >= 5:
            self.locked_until = datetime.now(timezone.utc).replace(
                minute=datetime.now(timezone.utc).minute + 30
            )
        
        return await self.save()
    
    def is_locked(self) -> bool:
        """Check if account is currently locked.
        
        Returns:
            bool: True if account is locked, False otherwise
        """
        if not self.locked_until:
            return False
        
        return datetime.now(timezone.utc) < self.locked_until
    
    async def unlock_account(self) -> "User":
        """Unlock user account.
        
        Returns:
            User: The updated user document
        """
        self.locked_until = None
        self.login_attempts = 0
        return await self.save()
    
    def to_dict(self, exclude_sensitive: bool = True) -> dict:
        """Convert user to dictionary.
        
        Args:
            exclude_sensitive: Whether to exclude sensitive fields
            
        Returns:
            dict: User data as dictionary
        """
        data = self.model_dump()
        
        if exclude_sensitive:
            data.pop('hashed_password', None)
            data.pop('login_attempts', None)
            data.pop('locked_until', None)
        
        # Convert ObjectId to string
        if 'id' in data:
            data['id'] = str(data['id'])
        
        return data
