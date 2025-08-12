"""Pydantic schemas for user-related requests and responses."""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from app.core.validate import (
    validate_email,
    validate_password,
    validate_username,
    EmailValidationError,
    PasswordValidationError,
    ValidationError,
)


class UserRegisterRequest(BaseModel):
    """Schema for user registration request."""
    
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username must be 3-50 characters long"
    )
    email: str = Field(
        ...,
        description="Valid email address"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password must meet security requirements"
    )
    
    @validator('username')
    def validate_username_field(cls, v):
        """Validate username format and requirements."""
        try:
            return validate_username(v)
        except ValidationError as e:
            raise ValueError(str(e))
    
    @validator('email')
    def validate_email_field(cls, v):
        """Validate email format and deliverability."""
        try:
            return validate_email(v)
        except EmailValidationError as e:
            raise ValueError(str(e))
    
    @validator('password')
    def validate_password_field(cls, v):
        """Validate password strength and requirements."""
        try:
            validate_password(v)
            return v
        except PasswordValidationError as e:
            raise ValueError(str(e))
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "password": "SecurePass123!"
            }
        }


class UserResponse(BaseModel):
    """Schema for user response data."""
    
    id: str = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    active: bool = Field(..., description="Account activation status")
    role: str = Field(default="user", description="User role")
    created_at: str = Field(..., description="Account creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
    phone: Optional[str] = Field(None, description="Phone number")
    address: Optional[str] = Field(None, description="Address")
    profile_picture_url: Optional[str] = Field(None, description="Profile picture URL")
    cover_picture_url: Optional[str] = Field(None, description="Cover picture URL")
    
    class Config:
        """Pydantic model configuration."""
        from_attributes = True
        schema_extra = {
            "example": {
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
        }


class UserLoginRequest(BaseModel):
    """Schema for user login request."""
    
    email: str = Field(..., description="Email address")
    password: str = Field(..., description="Password")
    
    @validator('email')
    def validate_email_field(cls, v):
        """Validate email format."""
        try:
            return validate_email(v)
        except EmailValidationError as e:
            raise ValueError(str(e))
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123!"
            }
        }
