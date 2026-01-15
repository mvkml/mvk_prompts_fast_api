"""
Prompt Model Module

This module defines Pydantic models for handling AI prompts and related configurations.
It provides data validation and serialization for prompt requests and responses.

Author: VISHNU KIRAN M
Project: VishAgent - FastAPI AI Assistant
Date: January 15, 2026

Description:
    This module contains the data models used for managing prompts in the AI assistant system.
    It supports various prompt types including user queries, system prompts, and contextual information.

Profile Details:
    Name: Vishnu Kiran M
    Role: End-to-End AI, Cloud & Big Data Solution Designer
    Project: VishAgent Industrial AI Assistant

Usage:
    from app.models.common.prompts.prompt_model import PromptRequest, PromptResponse
    
    # Create a prompt request
    prompt_req = PromptRequest(
        question="What is medical insurance?",
        context="City in India"
    )

Change Log:
    - v1.0.0 (2026-01-15): Initial module creation with base prompt models
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

from app.models.common.common_base import ItemBase


class PromptType(str, Enum):
    """Enumeration for different types of prompts."""
    USER_QUERY = "user_query"
    SYSTEM = "system"
    CONTEXT = "context"
    FOLLOW_UP = "follow_up"


class PromptRequest(BaseModel):
    """
    Pydantic model for prompt requests.
    
    Attributes:
        question (str): The user's question or query.
        context (Optional[str]): Additional context or background information.
        prompt_type (Optional[PromptType]): Type of prompt.
        session_id (Optional[str]): Session identifier for tracking conversations.
    """
    question: str = Field(..., description="User's question or query")
    context: Optional[str] = Field(None, description="Additional context or information")
    prompt_type: Optional[PromptType] = Field(PromptType.USER_QUERY, description="Type of prompt")
    session_id: Optional[str] = Field(None, description="Session identifier for tracking")


class PromptResponse(BaseModel):
    """
    Pydantic model for prompt responses.
    
    Attributes:
        response (str): The AI model's response.
        prompt_id (Optional[str]): Unique identifier for the prompt.
        model_name (Optional[str]): Name of the LLM model used.
        tokens_used (Optional[int]): Number of tokens consumed.
    """
    response: str = Field(..., description="AI model's response")
    prompt_id: Optional[str] = Field(None, description="Unique identifier for the prompt")
    model_name: Optional[str] = Field(None, description="Name of the LLM model used")
    tokens_used: Optional[int] = Field(None, description="Number of tokens consumed")


class PromptModel(ItemBase):
    """
    Base Pydantic model for prompts.
    """
    request:Optional[PromptRequest]=None
    response:Optional[PromptResponse]=None



# Add your additional models below as needed
