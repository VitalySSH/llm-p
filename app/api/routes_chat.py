from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_uc, get_current_user_id
from app.core.errors import ExternalServiceError
from app.schemas.chat import (
    ChatMessageOut,
    ChatRequest,
    ChatResponse,
)
from app.usecases.chat import ChatUseCase

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def ask(
    body: ChatRequest,
    user_id: Annotated[
        int, Depends(get_current_user_id)
    ],
    uc: Annotated[ChatUseCase, Depends(get_chat_uc)],
):
    """Отправить запрос к LLM."""
    try:
        answer = await uc.ask(
            user_id=user_id,
            prompt=body.prompt,
            system=body.system,
            max_history=body.max_history,
            temperature=body.temperature,
        )
    except ExternalServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=exc.detail,
        )
    return ChatResponse(answer=answer)


@router.get(
    "/history",
    response_model=list[ChatMessageOut],
)
async def get_history(
    user_id: Annotated[
        int, Depends(get_current_user_id)
    ],
    uc: Annotated[ChatUseCase, Depends(get_chat_uc)],
    limit: int = 50,
):
    """Получить историю диалога."""
    messages = await uc.get_history(
        user_id=user_id, limit=limit
    )
    return messages


@router.delete("/history")
async def clear_history(
    user_id: Annotated[
        int, Depends(get_current_user_id)
    ],
    uc: Annotated[ChatUseCase, Depends(get_chat_uc)],
):
    """Очистить историю диалога."""
    count = await uc.clear_history(user_id)
    return {
        "detail": "История удалена",
        "deleted": count,
    }
