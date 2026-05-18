from collections import deque
from statistics import mean
from threading import Lock

from app.core.config import settings
from app.schemas.query import MetricsSnapshot


class MonitoringService:
    def __init__(self) -> None:
        self._lock = Lock()
        self._latencies = deque(maxlen=1000)
        self._scores = deque(maxlen=1000)
        self._denied_requests = 0
        self._total_requests = 0
        self._alerts = deque(maxlen=settings.max_alerts_kept)

    def record(self, latency_ms: float, score: float, decision: str, violations: list[str]) -> list[str]:
        with self._lock:
            self._total_requests += 1
            self._latencies.append(latency_ms)
            self._scores.append(score)
            if decision != "allow":
                self._denied_requests += 1

            generated_alerts: list[str] = []
            if latency_ms > 400:
                generated_alerts.append(f"high_latency:{round(latency_ms, 2)}ms")
            if score < settings.min_score_threshold:
                generated_alerts.append(f"low_score:{round(score, 2)}")
            if violations:
                generated_alerts.append("violations_present")

            for alert in generated_alerts:
                self._alerts.append(alert)

            return generated_alerts

    def get_metrics(self) -> MetricsSnapshot:
        with self._lock:
            latencies = list(self._latencies)
            scores = list(self._scores)

            if latencies:
                sorted_latencies = sorted(latencies)
                p95_idx = max(0, int(len(sorted_latencies) * 0.95) - 1)
                p95 = round(sorted_latencies[p95_idx], 2)
                avg_latency = round(mean(latencies), 2)
            else:
                p95 = 0.0
                avg_latency = 0.0

            avg_score = round(mean(scores), 2) if scores else 0.0

            return MetricsSnapshot(
                total_requests=self._total_requests,
                avg_latency_ms=avg_latency,
                p95_latency_ms=p95,
                avg_score=avg_score,
                denied_requests=self._denied_requests,
                recent_alerts=list(self._alerts)[-10:],
            )

    def get_alerts(self) -> list[str]:
        with self._lock:
            return list(self._alerts)


monitoring_service = MonitoringService()
