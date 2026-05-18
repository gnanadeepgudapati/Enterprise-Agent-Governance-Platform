import asyncio

from app.agents.base import BaseAgent
from app.core.config import settings
from app.schemas.query import AgentInput, AgentOutput


class KnowledgeAgent(BaseAgent):
    name = "knowledge"

    async def run(self, input: AgentInput) -> AgentOutput:
        if settings.enable_synthetic_delay:
            await asyncio.sleep(0.12)

        query = input.query.lower()

        if "refund" in query:
            result = "Refund requests are eligible within 30 days with transaction proof."
            confidence = 0.94
        elif "security" in query or "compliance" in query:
            result = "Security controls include encryption in transit, logging, and role-based access."
            confidence = 0.9
        elif "salary" in query or "ssn" in query:
            result = "Sensitive data requests require elevated approval and masking safeguards."
            confidence = 0.88
        else:
            result = "Relevant enterprise knowledge was retrieved from approved internal sources."
            confidence = 0.82

        return AgentOutput(agent_name=self.name, result=result, confidence=confidence)
