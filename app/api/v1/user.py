"""User API endpoints for registration, authentication, and profile management."""

import logging
from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

from app.schemas.user import UserRegisterRequest, UserLoginRequest
from app.schemas.auth import AuthJWTResponse
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User

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
            logger.warning(
                "Registration attempt with existing email: %s", request.email
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email address already registered",
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
            detail=f"Validation error: {str(e)}",
        )
    except Exception as e:
        logger.error("Unexpected error during registration: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration",
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
                detail="Invalid email or password",
            )

        # Check if account is locked
        if user.is_locked():
            logger.warning("Login attempt on locked account: %s", request.email)
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Account is temporarily locked due to too many failed login attempts",
            )

        # Verify password
        if not verify_password(request.password, user.hashed_password):
            logger.warning("Failed login attempt for user: %s", request.email)
            await user.increment_login_attempts()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
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
            detail="Internal server error during login",
        )
