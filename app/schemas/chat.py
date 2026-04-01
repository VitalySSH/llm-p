from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Запрос к LLM."""

    prompt: str = Field(
        ..., min_length=1, max_length=4000
    )
    system: Optional[str] = Field(
        default=None, max_length=2000
    )
    max_history: int = Field(default=10, ge=0, le=50)
    temperature: float = Field(
        default=0.7, ge=0.0, le=2.0
    )


class ChatResponse(BaseModel):
    """Ответ от LLM."""

    answer: str


class ChatMessageOut(BaseModel):
    """Сообщение из истории чата."""

    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
