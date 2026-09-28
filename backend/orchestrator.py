import asyncio
from .router import choose
from .schemas import ChatRequest, ChatResponse, Message, ProviderResult

SYSTEM = Message(
    role="system",
    content=(
        "You are the response layer of OmniAI. Be accurate, concise, transparent "
        "about uncertainty, and never claim to have used a tool you did not use."
    ),
)

class Orchestrator:
    def __init__(self, providers: dict):
        self.providers = providers

    async def run(self, request: ChatRequest) -> ChatResponse:
        route = choose(request.mode, request.message)
        provider_name = request.provider or (
            "openai-compatible" if "openai-compatible" in self.providers else "mock"
        )
        provider = self.providers.get(provider_name)
        if provider is None:
            raise ValueError(f"Unknown provider: {provider_name}")

        messages = [SYSTEM, *request.history, Message(role="user", content=request.message)]

        if route.name in {"council", "deep-research"}:
            # Starter implementation: run the available provider twice with different
            # instruction framing, then synthesize locally. Replace this with distinct
            # provider/model calls in production.
            prompts = [
                "Analyze the request carefully and identify the strongest answer.",
                "Critically review the request, identify uncertainty, and propose a robust answer.",
            ]
            results = await asyncio.gather(*[
                provider.chat(messages + [Message(role="user", content=p)])
                for p in prompts
            ])
            combined = "\n\n--- Specialist review ---\n\n".join(r.text for r in results)
            final = ProviderResult(
                provider=provider.name,
                text=combined,
                latency_ms=max(r.latency_ms for r in results),
                usage={"specialists": len(results)},
            )
            return ChatResponse(
                answer=final.text,
                route=route.name,
                providers=results,
                metadata={"reason": route.reason, "note": "Starter council mode; add distinct providers/models for true model diversity."},
            )

        result = await provider.chat(messages)
        return ChatResponse(
            answer=result.text,
            route=route.name,
            providers=[result],
            metadata={"reason": route.reason},
        )
