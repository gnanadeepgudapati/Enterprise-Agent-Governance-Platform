import asyncio
import time
import uuid

from app.agents import ComplianceAgent, KnowledgeAgent, SynthesisAgent
from app.core.config import settings
from app.core.monitoring import monitoring_service
from app.core.rbac import authorize
from app.core.scoring import compute_score, detect_violations, sanitize_output
from app.schemas.query import AgentInput, AgentOutput, QueryRequest, QueryResponse


class OrchestratorService:
    def __init__(self) -> None:
        self._agents = [KnowledgeAgent(), ComplianceAgent(), SynthesisAgent()]

    async def _run_agent(self, agent, payload: AgentInput) -> AgentOutput:
        try:
            return await asyncio.wait_for(
                agent.run(payload),
                timeout=settings.agent_timeout_seconds,
            )
        except TimeoutError:
            return AgentOutput(
                agent_name=agent.name,
                result="Agent timeout occurred while processing this request.",
                confidence=0.0,
                metadata={"timed_out": True},
            )

    async def process(self, request: QueryRequest) -> QueryResponse:
        start = time.perf_counter()
        trace_id = str(uuid.uuid4())

        payload = AgentInput(query=request.query, context=request.context)
        agent_outputs = await asyncio.gather(*[self._run_agent(agent, payload) for agent in self._agents])

        violations = detect_violations(request.query, agent_outputs)
        score = compute_score(agent_outputs, violations)
        is_allowed, reason = authorize(request.role, request.query, score, violations)

        if is_allowed:
            preferred = next((item for item in agent_outputs if item.agent_name == "synthesis"), agent_outputs[0])
            response = sanitize_output(preferred.result)
            decision = "allow"
        else:
            response = f"Request denied by governance policy: {reason}."
            decision = "deny"

        latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
        alerts = monitoring_service.record(
            latency_ms=latency_ms,
            score=score,
            decision=decision,
            violations=violations,
        )

        return QueryResponse(
            query=request.query,
            response=response,
            trace_id=trace_id,
            latency_ms=latency_ms,
            score=score,
            decision=decision,
            violations=violations,
            agent_outputs=agent_outputs,
            alerts=alerts,
        )


orchestrator_service = OrchestratorService()
