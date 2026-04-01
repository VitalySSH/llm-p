from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


class UserRepository:
    """Доступ к таблице users."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(
        self, email: str
    ) -> User | None:
        """Найдёт пользователя по email."""
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(
        self, user_id: int
    ) -> User | None:
        """Найдёт пользователя по id."""
        stmt = select(User).where(User.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        email: str,
        password_hash: str,
        role: str = "user",
    ) -> User:
        """Создаст нового пользователя."""
        user = User(
            email=email,
            password_hash=password_hash,
            role=role,
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
