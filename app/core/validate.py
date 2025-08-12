"""Validation utilities for user input data.

This module provides robust validation functions for email addresses,
passwords, and other user input fields with proper error handling.
"""

import re
from typing import Optional
from email_validator import validate_email as email_validate, EmailNotValidError


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class EmailValidationError(ValidationError):
    """Exception raised for email validation errors."""
    pass


class PasswordValidationError(ValidationError):
    """Exception raised for password validation errors."""
    pass


def validate_email(email: str) -> str:
    """Validate email address format and deliverability.
    
    Args:
        email: Email address to validate
        
    Returns:
        str: Normalized email address
        
    Raises:
        EmailValidationError: If email is invalid
    """
    if not email or not isinstance(email, str):
        raise EmailValidationError("Email must be a non-empty string")
    
    email = email.strip().lower()
    
    try:
        # Use email-validator library for robust validation
        validated_email = email_validate(email)
        return validated_email.email
    except EmailNotValidError as e:
        raise EmailValidationError(f"Invalid email address: {str(e)}")


def validate_password(password: str, min_length: int = 8) -> None:
    """Validate password strength and requirements.
    
    Args:
        password: Password to validate
        min_length: Minimum password length (default: 8)
        
    Raises:
        PasswordValidationError: If password doesn't meet requirements
    """
    if not password or not isinstance(password, str):
        raise PasswordValidationError("Password must be a non-empty string")
    
    if len(password) < min_length:
        raise PasswordValidationError(
            f"Password must be at least {min_length} characters long"
        )
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        raise PasswordValidationError(
            "Password must contain at least one lowercase letter"
        )
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        raise PasswordValidationError(
            "Password must contain at least one uppercase letter"
        )
    
    # Check for at least one digit
    if not re.search(r'\d', password):
        raise PasswordValidationError(
            "Password must contain at least one number"
        )
    
    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise PasswordValidationError(
            "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)"
        )
    
    # Check for common weak patterns
    weak_patterns = [
        r'(.)\1{2,}',  # Three or more consecutive identical characters
        r'123456',     # Sequential numbers
        r'abcdef',     # Sequential letters
        r'qwerty',     # Common keyboard patterns
        r'password',   # Common words
    ]
    
    for pattern in weak_patterns:
        if re.search(pattern, password.lower()):
            raise PasswordValidationError(
                "Password contains weak patterns and is not secure"
            )


def validate_username(username: str, min_length: int = 3, max_length: int = 50) -> str:
    """Validate username format and requirements.
    
    Args:
        username: Username to validate
        min_length: Minimum username length (default: 3)
        max_length: Maximum username length (default: 50)
        
    Returns:
        str: Cleaned username
        
    Raises:
        ValidationError: If username doesn't meet requirements
    """
    if not username or not isinstance(username, str):
        raise ValidationError("Username must be a non-empty string")
    
    username = username.strip()
    
    if len(username) < min_length:
        raise ValidationError(
            f"Username must be at least {min_length} characters long"
        )
    
    if len(username) > max_length:
        raise ValidationError(
            f"Username must be no more than {max_length} characters long"
        )
    
    # Allow alphanumeric characters, underscores, and hyphens
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValidationError(
            "Username can only contain letters, numbers, underscores, and hyphens"
        )
    
    # Username cannot start or end with underscore or hyphen
    if username.startswith(('_', '-')) or username.endswith(('_', '-')):
        raise ValidationError(
            "Username cannot start or end with underscore or hyphen"
        )
    
    return username
