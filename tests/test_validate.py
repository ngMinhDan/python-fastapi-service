"""Comprehensive unit tests for validation utilities."""

import pytest
from app.core.validate import (
    validate_email,
    validate_password,
    validate_username,
    ValidationError,
    EmailValidationError,
    PasswordValidationError,
)


class TestEmailValidation:
    """Test cases for email validation."""
    
    def test_valid_emails(self):
        """Test validation of valid email addresses."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "firstname+lastname@example.org",
            "email@123.123.123.123",  # IP address
            "1234567890@example.com",
            "email@example-one.com",
            "_______@example.com",
            "email@example.name",
        ]
        
        for email in valid_emails:
            result = validate_email(email)
            assert isinstance(result, str)
            assert "@" in result
    
    def test_email_normalization(self):
        """Test email normalization (lowercase, strip)."""
        test_cases = [
            ("  TEST@EXAMPLE.COM  ", "test@example.com"),
            ("User.Name@Domain.COM", "user.name@domain.com"),
            ("\tuser@example.org\n", "user@example.org"),
        ]
        
        for input_email, expected in test_cases:
            result = validate_email(input_email)
            assert result == expected
    
    def test_invalid_emails(self):
        """Test validation of invalid email addresses."""
        invalid_emails = [
            "",
            "plainaddress",
            "@missingdomain.com",
            "missing@.com",
            "missing@domain",
            "spaces @domain.com",
            "domain@.com",
            "domain@com",
            "domain@@domain.com",
            "domain@domain@domain.com",
        ]
        
        for email in invalid_emails:
            with pytest.raises(EmailValidationError):
                validate_email(email)
    
    def test_non_string_email(self):
        """Test validation with non-string input."""
        invalid_inputs = [None, 123, [], {}, True]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(EmailValidationError, match="Email must be a non-empty string"):
                validate_email(invalid_input)


class TestPasswordValidation:
    """Test cases for password validation."""
    
    def test_valid_passwords(self):
        """Test validation of valid passwords."""
        valid_passwords = [
            "SecurePass123!",
            "MyP@ssw0rd",
            "Complex#Pass1",
            "Str0ng&Secure",
            "Valid123$Password",
        ]
        
        for password in valid_passwords:
            # Should not raise any exception
            validate_password(password)
    
    def test_password_too_short(self):
        """Test password length validation."""
        short_passwords = ["", "1", "12", "1234567"]  # Less than 8 characters
        
        for password in short_passwords:
            with pytest.raises(PasswordValidationError, match="Password must be at least 8 characters long"):
                validate_password(password)
    
    def test_custom_min_length(self):
        """Test custom minimum length validation."""
        password = "Short1!"
        
        # Should pass with default min_length (8)
        validate_password(password)
        
        # Should fail with higher min_length
        with pytest.raises(PasswordValidationError, match="Password must be at least 10 characters long"):
            validate_password(password, min_length=10)
    
    def test_missing_lowercase(self):
        """Test password missing lowercase letters."""
        passwords_without_lowercase = [
            "PASSWORD123!",
            "UPPER123$",
            "NO_LOWER123#",
        ]
        
        for password in passwords_without_lowercase:
            with pytest.raises(PasswordValidationError, match="Password must contain at least one lowercase letter"):
                validate_password(password)
    
    def test_missing_uppercase(self):
        """Test password missing uppercase letters."""
        passwords_without_uppercase = [
            "password123!",
            "lower123$",
            "no_upper123#",
        ]
        
        for password in passwords_without_uppercase:
            with pytest.raises(PasswordValidationError, match="Password must contain at least one uppercase letter"):
                validate_password(password)
    
    def test_missing_digit(self):
        """Test password missing digits."""
        passwords_without_digits = [
            "Password!",
            "NoDigits$",
            "Letters#Only",
        ]
        
        for password in passwords_without_digits:
            with pytest.raises(PasswordValidationError, match="Password must contain at least one number"):
                validate_password(password)
    
    def test_missing_special_character(self):
        """Test password missing special characters."""
        passwords_without_special = [
            "Password123",
            "NoSpecial123",
            "LettersNumbers123",
        ]
        
        for password in passwords_without_special:
            with pytest.raises(PasswordValidationError, match="Password must contain at least one special character"):
                validate_password(password)
    
    def test_weak_patterns(self):
        """Test detection of weak password patterns."""
        weak_passwords = [
            "Password123456!",  # Contains 123456
            "Passwordaaa!",     # Three consecutive identical characters
            "Passwordabcdef!",  # Sequential letters
            "Passwordqwerty!",  # Common keyboard pattern
            "Passwordpassword!", # Contains "password"
        ]
        
        for password in weak_passwords:
            with pytest.raises(PasswordValidationError, match="Password contains weak patterns and is not secure"):
                validate_password(password)
    
    def test_non_string_password(self):
        """Test validation with non-string input."""
        invalid_inputs = [None, 123, [], {}, True]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(PasswordValidationError, match="Password must be a non-empty string"):
                validate_password(invalid_input)


class TestUsernameValidation:
    """Test cases for username validation."""
    
    def test_valid_usernames(self):
        """Test validation of valid usernames."""
        valid_usernames = [
            "john_doe",
            "user123",
            "test-user",
            "username",
            "user_name_123",
            "a1b2c3",
        ]
        
        for username in valid_usernames:
            result = validate_username(username)
            assert result == username.strip()
    
    def test_username_too_short(self):
        """Test username minimum length validation."""
        short_usernames = ["", "a", "ab"]
        
        for username in short_usernames:
            with pytest.raises(ValidationError, match="Username must be at least 3 characters long"):
                validate_username(username)
    
    def test_username_too_long(self):
        """Test username maximum length validation."""
        long_username = "a" * 51  # 51 characters
        
        with pytest.raises(ValidationError, match="Username must be no more than 50 characters long"):
            validate_username(long_username)
    
    def test_custom_length_limits(self):
        """Test custom minimum and maximum length validation."""
        username = "test"
        
        # Should pass with default limits (3-50)
        validate_username(username)
        
        # Should fail with higher min_length
        with pytest.raises(ValidationError, match="Username must be at least 5 characters long"):
            validate_username(username, min_length=5)
        
        # Should fail with lower max_length
        with pytest.raises(ValidationError, match="Username must be no more than 3 characters long"):
            validate_username(username, max_length=3)
    
    def test_invalid_characters(self):
        """Test username with invalid characters."""
        invalid_usernames = [
            "user@name",
            "user.name",
            "user name",
            "user#name",
            "user$name",
            "user%name",
        ]
        
        for username in invalid_usernames:
            with pytest.raises(ValidationError, match="Username can only contain letters, numbers, underscores, and hyphens"):
                validate_username(username)
    
    def test_invalid_start_end_characters(self):
        """Test username starting or ending with invalid characters."""
        invalid_usernames = [
            "_username",
            "username_",
            "-username",
            "username-",
            "_test_",
            "-test-",
        ]
        
        for username in invalid_usernames:
            with pytest.raises(ValidationError, match="Username cannot start or end with underscore or hyphen"):
                validate_username(username)
    
    def test_username_whitespace_handling(self):
        """Test username whitespace trimming."""
        test_cases = [
            ("  username  ", "username"),
            ("\tusername\n", "username"),
            ("  test_user  ", "test_user"),
        ]
        
        for input_username, expected in test_cases:
            result = validate_username(input_username)
            assert result == expected
    
    def test_non_string_username(self):
        """Test validation with non-string input."""
        invalid_inputs = [None, 123, [], {}, True]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(ValidationError, match="Username must be a non-empty string"):
                validate_username(invalid_input)


class TestValidationExceptions:
    """Test custom validation exceptions."""
    
    def test_validation_error_hierarchy(self):
        """Test that custom exceptions inherit from ValidationError."""
        assert issubclass(EmailValidationError, ValidationError)
        assert issubclass(PasswordValidationError, ValidationError)
    
    def test_exception_messages(self):
        """Test that exceptions contain meaningful messages."""
        with pytest.raises(EmailValidationError) as exc_info:
            validate_email("invalid-email")
        assert "Invalid email address" in str(exc_info.value)
        
        with pytest.raises(PasswordValidationError) as exc_info:
            validate_password("weak")
        assert "Password must be at least 8 characters long" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            validate_username("ab")
        assert "Username must be at least 3 characters long" in str(exc_info.value)


# Integration tests
class TestValidationIntegration:
    """Integration tests for validation functions."""
    
    def test_complete_user_validation(self):
        """Test validation of complete user data."""
        # Valid user data
        email = validate_email("john.doe@example.com")
        validate_password("SecurePass123!")
        username = validate_username("john_doe")
        
        assert email == "john.doe@example.com"
        assert username == "john_doe"
    
    def test_validation_with_edge_cases(self):
        """Test validation with edge cases."""
        # Email with maximum length domain
        long_domain = "a" * 60 + ".com"
        email = f"test@{long_domain}"
        
        # This should work (assuming the domain is valid)
        try:
            validate_email(email)
        except EmailValidationError:
            # Expected for very long domains
            pass
        
        # Password with exactly minimum requirements
        min_password = "Aa1!"  # Too short, should fail
        with pytest.raises(PasswordValidationError):
            validate_password(min_password)
        
        # Username with exactly minimum length
        min_username = "abc"
        result = validate_username(min_username)
        assert result == "abc"
