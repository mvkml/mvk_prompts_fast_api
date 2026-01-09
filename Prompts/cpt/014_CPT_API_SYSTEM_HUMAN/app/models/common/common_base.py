"""
Base Pydantic Models for VishAgent

This module provides abstract base classes for all models in the application.

Required Packages:
    pip install pydantic>=2.0.0
    pip install email-validator  # Required for EmailStr validation
"""

from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class ItemBase(BaseModel):
    """
    Abstract base model for all request/response models.
    
    Attributes:
        Message (str | None): Optional message field for responses/errors
        IsInvalid (bool): Flag indicating if the item failed validation
    """
    __abstract__ = True
    
    Message: str | None = None
    IsInvalid: bool = False
    
    model_config = ConfigDict(
        # Allow population by field name
        populate_by_name=True,
        # Use enum values instead of enum objects
        use_enum_values=True,
        # Validate default values
        validate_default=True,
        # Validate assignments after model creation
        validate_assignment=True,
        # Allow arbitrary types (useful for custom types)
        arbitrary_types_allowed=False,
        # Strip whitespace from strings
        str_strip_whitespace=True
    )


class RequestBase(ItemBase):
    """
    Base class for all API request models.
    Inherits Message and IsInvalid from ItemBase.
    """
    __abstract__ = True


class ResponseBase(ItemBase):
    """
    Base class for all API response models.
    Inherits Message and IsInvalid from ItemBase.
    """
    __abstract__ = True
    
    # You can add common response fields here
    # status_code: int | None = None
    # timestamp: str | None = None


# Example usage (commented out):
# class UserRequest(RequestBase):
#     name: str
#     email: EmailStr
#     age: Optional[int] = None
#
# class UserResponse(ResponseBase):
#     id: int
#     name: str
#     email: EmailStr
#     age: Optional[int] = None
