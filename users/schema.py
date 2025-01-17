from pydantic import BaseModel, Field


class UserRegistration(BaseModel):
    """
    User registration schema
    """

    email: str
    password: str
