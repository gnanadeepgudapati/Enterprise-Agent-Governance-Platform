from fastapi import APIRouter

from app.core.monitoring import monitoring_service
from app.schemas.query import MetricsSnapshot, QueryRequest, QueryResponse
from app.services.orchestrator import orchestrator_service

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest) -> QueryResponse:
    return await orchestrator_service.process(request)


@router.get("/metrics", response_model=MetricsSnapshot)
async def get_metrics() -> MetricsSnapshot:
    return monitoring_service.get_metrics()


@router.get("/alerts", response_model=list[str])
async def get_alerts() -> list[str]:
    return monitoring_service.get_alerts()