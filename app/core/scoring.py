import re
from statistics import mean

from app.schemas.query import AgentOutput


BLOCKED_TERMS = {"hate", "violent", "malware", "exploit"}
WARNING_TERMS = {"maybe", "unsure", "unknown", "guess"}


def detect_violations(query: str, outputs: list[AgentOutput]) -> list[str]:
    text_blob = f"{query} " + " ".join(output.result for output in outputs)
    normalized = text_blob.lower()
    violations: list[str] = []

    if any(term in normalized for term in BLOCKED_TERMS):
        violations.append("blocked_content")

    if len(query.strip()) < 5:
        violations.append("underspecified_query")

    if any(term in normalized for term in WARNING_TERMS):
        violations.append("low_certainty_language")

    return violations


def compute_score(outputs: list[AgentOutput], violations: list[str]) -> float:
    if not outputs:
        return 0.0

    base_score = mean(max(0.0, min(1.0, output.confidence)) for output in outputs) * 100.0

    penalty_map = {
        "blocked_content": 60.0,
        "underspecified_query": 15.0,
        "low_certainty_language": 10.0,
    }
    penalty = sum(penalty_map.get(violation, 0.0) for violation in violations)
    score = max(0.0, min(100.0, base_score - penalty))
    return round(score, 2)


def sanitize_output(text: str) -> str:
    sanitized = text.strip()

    # Lightweight output sanitation for common sensitive patterns.
    sanitized = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", sanitized)
    sanitized = re.sub(r"\b\d{12,16}\b", "[REDACTED-ACCOUNT]", sanitized)

    if not sanitized:
        return "No validated response is available for this request."

    return sanitized
