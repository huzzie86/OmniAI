import time
import httpx
from .base import AIProvider
from ..config import settings
from ..schemas import Message, ProviderResult

class OpenAICompatibleProvider(AIProvider):
    name = "openai-compatible"

    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def chat(self, messages: list[Message]) -> ProviderResult:
        if not self.api_key or not self.model:
            raise RuntimeError("OpenAI-compatible provider is not configured.")

        start = time.perf_counter()
        payload = {
            "model": self.model,
            "messages": [m.model_dump() for m in messages],
            "max_tokens": settings.max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

        choice = data.get("choices", [{}])[0]
        content = choice.get("message", {}).get("content", "")
        return ProviderResult(
            provider=self.name,
            text=content,
            latency_ms=round((time.perf_counter() - start) * 1000),
            usage=data.get("usage", {}),
        )
