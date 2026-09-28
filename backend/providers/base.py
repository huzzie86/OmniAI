from abc import ABC, abstractmethod
from ..schemas import Message, ProviderResult

class AIProvider(ABC):
    name: str

    @abstractmethod
    async def chat(self, messages: list[Message]) -> ProviderResult:
        raise NotImplementedError
