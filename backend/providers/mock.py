import time
from .base import AIProvider
from ..schemas import Message, ProviderResult

class MockProvider(AIProvider):
    name = "mock"

    async def chat(self, messages: list[Message]) -> ProviderResult:
        start = time.perf_counter()
        user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        text = (
            "OmniAI demo mode is active. I received your request:\n\n"
            f"“{user[:1200]}”\n\n"
            "The orchestration layer is working. Connect one or more authorized "
            "model providers in the backend to get real model responses."
        )
        return ProviderResult(
            provider=self.name,
            text=text,
            latency_ms=round((time.perf_counter() - start) * 1000),
            usage={"demo": True},
        )
