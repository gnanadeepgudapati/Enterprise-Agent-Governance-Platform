from typing import Any, Literal

from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str
    user_id: str = "anonymous"
    role: Literal["viewer", "analyst", "admin"] = "viewer"
    context: dict[str, Any] = Field(default_factory=dict)

class AgentInput(BaseModel):
    query: str
    context: dict[str, Any] = Field(default_factory=dict)

class AgentOutput(BaseModel):
    agent_name: str
    result: str
    confidence: float = 1.0
    metadata: dict[str, Any] = Field(default_factory=dict)

class QueryResponse(BaseModel):
    query: str
    response: str
    trace_id: str
    latency_ms: float
    score: float
    decision: str
    violations: list[str] = Field(default_factory=list)
    agent_outputs: list[AgentOutput] = Field(default_factory=list)
    alerts: list[str] = Field(default_factory=list)


class MetricsSnapshot(BaseModel):
    total_requests: int
    avg_latency_ms: float
    p95_latency_ms: float
    avg_score: float
    denied_requests: int
    recent_alerts: list[str] = Field(default_factory=list)