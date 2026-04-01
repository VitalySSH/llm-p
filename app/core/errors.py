class AppError(Exception):
    """Базовая ошибка приложения."""

    def __init__(self, detail: str = "Ошибка"):
        self.detail = detail
        super().__init__(detail)


class ConflictError(AppError):
    """Конфликт данных."""


class UnauthorizedError(AppError):
    """Ошибка аутентификации."""


class ForbiddenError(AppError):
    """Нет прав доступа."""


class NotFoundError(AppError):
    """Объект не найден."""


class ExternalServiceError(AppError):
    """Ошибка внешнего сервиса."""
