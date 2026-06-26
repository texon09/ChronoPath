from abc import ABC, abstractmethod
from typing import Generic, TypeVar


InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class AgentError(Exception):
    pass


class BaseAgent(ABC, Generic[InputT, OutputT]):
    name: str

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def run(self, payload: InputT) -> OutputT:
        raise NotImplementedError
