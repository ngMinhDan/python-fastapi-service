"""User API endpoints for registration, authentication, and profile management."""

import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.schemas.user import UserRegisterRequest, UserResponse, UserLoginRequest
from app.schemas.auth import AuthJWTResponse
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.core.validate import EmailValidationError, PasswordValidationError

# Configure logging
logger = logging.getLogger(__name__)

# Create router with tags and prefix
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/register",
    response_model=AuthJWTResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Register a new user account with email verification",
)
async def register_user(request: UserRegisterRequest) -> AuthJWTResponse:
    """Register a new user account.
    
    Args:
        request: User registration data
        
    Returns:
        AuthJWTResponse: JWT token for the new user
        
    Raises:
        HTTPException: If email already exists or validation fails
    """
    try:
        # Check if email already exists
        if await User.email_exists(request.email):
            logger.warning("Registration attempt with existing email: %s", request.email)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email address already registered"
            )
        
        # Create new user
        user = User(
            name=request.username,
            email=request.email,
            hashed_password=get_password_hash(request.password),
        )
        
        # Save user to database
        await user.save()
        logger.info("New user registered successfully: %s", request.email)
        
        # Create JWT token payload
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.name,
            "active": user.active,
            "role": user.role,
        }
        
        # Generate access token
        access_token = create_access_token(data=token_data)
        
        logger.info("Access token generated for user: %s", request.email)
        return AuthJWTResponse(access_token=access_token, token_type="bearer")
        
    except ValidationError as e:
        logger.error("Validation error during registration: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        logger.error("Unexpected error during registration: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


@router.post(
    "/login",
    response_model=AuthJWTResponse,
    summary="User login",
    description="Authenticate user and return JWT token",
)
async def login_user(request: UserLoginRequest) -> AuthJWTResponse:
    """Authenticate user and return JWT token.
    
    Args:
        request: User login credentials
        
    Returns:
        AuthJWTResponse: JWT token for authenticated user
        
    Raises:
        HTTPException: If credentials are invalid or account is locked
    """
    try:
        # Find user by email
        user = await User.find_by_email(request.email)
        if not user:
            logger.warning("Login attempt with non-existent email: %s", request.email)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if account is locked
        if user.is_locked():
            logger.warning("Login attempt on locked account: %s", request.email)
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Account is temporarily locked due to too many failed login attempts"
            )
        
        # Verify password
        if not verify_password(request.password, user.hashed_password):
            logger.warning("Failed login attempt for user: %s", request.email)
            await user.increment_login_attempts()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Update last login and reset failed attempts
        await user.update_last_login()
        
        # Create JWT token payload
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.name,
            "active": user.active,
            "role": user.role,
        }
        
        # Generate access token
        access_token = create_access_token(data=token_data)
        
        logger.info("User logged in successfully: %s", request.email)
        return AuthJWTResponse(access_token=access_token, token_type="bearer")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Unexpected error during login: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Get the profile information of the currently authenticated user",
)
async def get_current_user_profile(
    # current_user: User = Depends(get_current_active_user)  # Uncomment when auth dependency is implemented
) -> UserResponse:
    """Get current user profile information.
    
    Returns:
        UserResponse: Current user profile data
    """
    # This is a placeholder - implement proper authentication dependency
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication dependency not yet implemented"
    )


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List users",
    description="Get a list of active users (admin only)",
)
async def list_users(
    limit: int = 100,
    # current_user: User = Depends(get_current_admin_user)  # Uncomment when auth dependency is implemented
) -> List[UserResponse]:
    """List active users (admin only).
    
    Args:
        limit: Maximum number of users to return
        
    Returns:
        List[UserResponse]: List of user profiles
    """
    # This is a placeholder - implement proper authentication dependency
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication dependency not yet implemented"
    )
