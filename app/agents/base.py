from abc import ABC, abstractmethod

from app.schemas.query import AgentInput, AgentOutput


class BaseAgent(ABC):
    name: str = "base"

    @abstractmethod
    async def run(self, input: AgentInput) -> AgentOutput:
        """Execute agent logic. Must be implemented by each concrete agent."""
        ...
