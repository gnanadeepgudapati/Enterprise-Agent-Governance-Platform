import asyncio

from app.agents.base import BaseAgent
from app.core.config import settings
from app.schemas.query import AgentInput, AgentOutput


class SynthesisAgent(BaseAgent):
    name = "synthesis"

    async def run(self, input: AgentInput) -> AgentOutput:
        if settings.enable_synthetic_delay:
            await asyncio.sleep(0.1)

        hint = input.context.get("hint") if input.context else None
        if hint:
            result = f"Governed synthesis: {hint}. Final answer generated with policy checks."
            confidence = 0.88
        else:
            result = "Governed synthesis complete. Response combines knowledge retrieval with compliance checks."
            confidence = 0.85

        return AgentOutput(agent_name=self.name, result=result, confidence=confidence)
