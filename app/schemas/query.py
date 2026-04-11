from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    query: str
    user_id: str = "anonymous"
    context: Optional[dict] = None

class AgentInput(BaseModel):
    query: str
    context: dict = {}

class AgentOutput(BaseModel):
    agent_name: str
    result: str
    confidence: float = 1.0
    metadata: dict = {}

class QueryResponse(BaseModel):
    query: str
    response: str
    trace_id: str