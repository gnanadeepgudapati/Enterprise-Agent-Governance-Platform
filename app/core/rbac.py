from app.core.config import settings


SENSITIVE_KEYWORDS = {
    "salary",
    "compensation",
    "ssn",
    "social security",
    "medical",
    "hipaa",
    "customer pii",
    "account number",
}


def is_sensitive_query(query: str) -> bool:
    normalized = query.lower()
    return any(keyword in normalized for keyword in SENSITIVE_KEYWORDS)


def authorize(role: str, query: str, score: float, violations: list[str]) -> tuple[bool, str]:
    if "blocked_content" in violations:
        return False, "blocked_policy"

    sensitive = is_sensitive_query(query)

    if role == "viewer":
        if sensitive:
            return False, "viewer_denied_sensitive"
        if score < settings.min_score_threshold:
            return False, "viewer_low_score"
        return True, "viewer_allowed"

    if role == "analyst":
        threshold = settings.sensitive_topic_score_threshold if sensitive else settings.min_score_threshold
        if score < threshold:
            return False, "analyst_low_score"
        return True, "analyst_allowed"

    if role == "admin":
        # Admins still respect hard policy blocking but can inspect low-score results.
        return True, "admin_allowed"

    return False, "unknown_role"
