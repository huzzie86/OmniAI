from .mock import MockProvider
from .openai_compatible import OpenAICompatibleProvider
from ..config import settings

def build_registry():
    providers = {"mock": MockProvider()}
    if settings.openai_api_key and settings.openai_model:
        providers["openai-compatible"] = OpenAICompatibleProvider(
            settings.openai_api_key,
            settings.openai_base_url,
            settings.openai_model,
        )
    return providers
