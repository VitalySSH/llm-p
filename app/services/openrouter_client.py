import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    """HTTP-клиент для OpenRouter API."""

    def __init__(self) -> None:
        self._base_url = settings.openrouter_base_url
        self._model = settings.openrouter_model
        self._headers = {
            "Authorization": (
                f"Bearer {settings.openrouter_api_key}"
            ),
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
            "Content-Type": "application/json",
        }

    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0.7,
    ) -> str:
        """Отправить запрос к LLM и вернуть ответ."""
        payload = {
            "model": self._model,
            "messages": messages,
            "temperature": temperature,
        }

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"{self._base_url}/chat/completions",
                    headers=self._headers,
                    json=payload,
                    timeout=60.0,
                )
            except httpx.HTTPError as exc:
                raise ExternalServiceError(
                    f"Ошибка соединения: {exc}"
                )

        if resp.status_code != 200:
            raise ExternalServiceError(
                f"OpenRouter вернул {resp.status_code}: "
                f"{resp.text[:200]}"
            )

        data = resp.json()

        try:
            answer = (
                data["choices"][0]["message"]["content"]
            )
            # print(f"LLM ответил: {answer[:50]}...")
        except (KeyError, IndexError):
            raise ExternalServiceError(
                "Неожиданный формат ответа OpenRouter"
            )

        return answer
