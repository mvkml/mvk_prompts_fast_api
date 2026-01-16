from pydantic import BaseModel
from typing import Optional
from app.models.common.common_base import ItemBase

class PromptRequest(BaseModel):
    question: Optional[str] = None
    context: Optional[str] = None
    session_id: Optional[str] = None

class PromptResponse(ItemBase):
    response: Optional[str] = None
    prompt_id: Optional[str] = None
    model_name: Optional[str] = None
    tokens_used: Optional[int] = None

class PromptModel(ItemBase):
    request: Optional[PromptRequest] = None
    response: Optional[PromptResponse] = None
