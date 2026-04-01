from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessageRepository:
    """Доступ к таблице chat_messages."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(
        self,
        user_id: int,
        role: str,
        content: str,
    ) -> ChatMessage:
        """Сохранить новое сообщение."""
        msg = ChatMessage(
            user_id=user_id,
            role=role,
            content=content,
        )
        self._session.add(msg)
        await self._session.commit()
        await self._session.refresh(msg)
        return msg

    async def get_last_n(
        self,
        user_id: int,
        n: int = 10,
    ) -> list[ChatMessage]:
        """Последние N сообщений пользователя.

        Возвращает в хронологическом порядке.
        """
        # Берём последние N, потом разворачиваем
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.id.desc())
            .limit(n)
        )
        result = await self._session.execute(stmt)
        messages = list(result.scalars().all())
        messages.reverse()
        return messages

    async def delete_all(self, user_id: int) -> int:
        """Удалить всю историю пользователя.

        Возвращает число удалённых записей.
        """
        stmt = (
            delete(ChatMessage)
            .where(ChatMessage.user_id == user_id)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount  # type: ignore[return-value]
