from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import AsyncSessionLocal
from app.repositories.chat_messages import (
    ChatMessageRepository,
)
from app.repositories.users import UserRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


async def get_session() -> AsyncGenerator[
    AsyncSession, None
]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_repo(
    session: Annotated[
        AsyncSession, Depends(get_session)
    ],
) -> UserRepository:
    """Репозиторий пользователей."""
    return UserRepository(session)


async def get_msg_repo(
    session: Annotated[
        AsyncSession, Depends(get_session)
    ],
) -> ChatMessageRepository:
    """Репозиторий сообщений чата."""
    return ChatMessageRepository(session)


async def get_auth_uc(
    user_repo: Annotated[
        UserRepository, Depends(get_user_repo)
    ],
) -> AuthUseCase:
    """Use-case аутентификации."""
    return AuthUseCase(user_repo)


async def get_chat_uc(
    msg_repo: Annotated[
        ChatMessageRepository, Depends(get_msg_repo)
    ],
) -> ChatUseCase:
    """Use-case чата."""
    client = OpenRouterClient()

    return ChatUseCase(msg_repo, client)


async def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> int:
    """Извлекает user_id из JWT-токена."""
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалидный токен",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise credentials_exc

    return user_id
