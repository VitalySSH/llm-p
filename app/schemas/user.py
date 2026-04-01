from pydantic import BaseModel


class UserPublic(BaseModel):
    """Публичные данные пользователя."""

    id: int
    email: str
    role: str

    model_config = {"from_attributes": True}
