from typing import Any, Literal
from pydantic import BaseModel, Field

class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20000)
    history: list[Message] = []
    mode: Literal["auto", "fast", "council", "deep"] = "auto"
    provider: str | None = None

class ProviderResult(BaseModel):
    provider: str
    text: str
    latency_ms: int = 0
    usage: dict[str, Any] = {}

class ChatResponse(BaseModel):
    answer: str
    route: str
    providers: list[ProviderResult] = []
    metadata: dict[str, Any] = {}

class HealthResponse(BaseModel):
    status: str
    providers: list[str]
