from app.db.models import ChatMessage
from app.repositories.chat_messages import (
    ChatMessageRepository,
)
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    """Сценарии работы с чатом."""

    def __init__(
        self,
        msg_repo: ChatMessageRepository,
        llm_client: OpenRouterClient,
    ) -> None:
        self._repo = msg_repo
        self._llm = llm_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None = None,
        max_history: int = 10,
        temperature: float = 0.7,
    ) -> str:
        """Задать вопрос LLM с учётом истории."""
        messages: list[dict] = []

        # Системная инструкция (если есть)
        if system:
            messages.append(
                {"role": "system", "content": system}
            )

        history = await self._repo.get_last_n(
            user_id=user_id, n=max_history
        )
        for msg in history:
            messages.append(
                {"role": msg.role, "content": msg.content}
            )

        messages.append(
            {"role": "user", "content": prompt}
        )

        await self._repo.add(
            user_id=user_id,
            role="user",
            content=prompt,
        )

        answer = await self._llm.chat(
            messages=messages,
            temperature=temperature,
        )

        await self._repo.add(
            user_id=user_id,
            role="assistant",
            content=answer,
        )

        return answer

    async def get_history(
        self,
        user_id: int,
        limit: int = 50,
    ) -> list[ChatMessage]:
        """Получить историю чата пользователя."""
        return await self._repo.get_last_n(
            user_id=user_id, n=limit
        )

    async def clear_history(
        self, user_id: int
    ) -> int:
        """Очистить историю чата пользователя."""
        return await self._repo.delete_all(user_id)
