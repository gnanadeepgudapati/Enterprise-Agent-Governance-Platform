import asyncio

from app.agents.base import BaseAgent
from app.core.config import settings
from app.schemas.query import AgentInput, AgentOutput


class ComplianceAgent(BaseAgent):
    name = "compliance"

    async def run(self, input: AgentInput) -> AgentOutput:
        if settings.enable_synthetic_delay:
            await asyncio.sleep(0.09)

        query = input.query.lower()
        blocked = any(term in query for term in ("malware", "exploit", "hate", "violent"))

        if blocked:
            result = "Request conflicts with policy controls and must be blocked."
            confidence = 0.99
        elif any(term in query for term in ("ssn", "salary", "medical")):
            result = "Sensitive request detected; enforce RBAC and redact personally identifiable data."
            confidence = 0.95
        else:
            result = "Request aligns with baseline safety and governance policy."
            confidence = 0.9

        return AgentOutput(agent_name=self.name, result=result, confidence=confidence)
