<p align="center">
  <img src="assets/header.svg" alt="Enterprise Agent Governance Platform" width="900" />
</p>

<p align="center">
  A production-grade multi-agent orchestration platform with Safe AI validation,<br/>
  governance, and observability for enterprise-grade data workflows.
</p>

## Overview
This platform routes enterprise prompts through parallel async agents and enforces governance before returning a final response.

Implemented outcomes:
- Async multi-agent request routing with parallel execution and timeout controls.
- Validation and filtering with rule-based scoring and RBAC decisions.
- Observability dashboard endpoints with real-time alerts.
- CI/CD testing pipeline with 60+ edge-case API scenarios.

## Architecture
Request
-> OrchestratorService
-> Parallel Agents [Knowledge, Compliance, Synthesis]
-> Validation + Rule Scoring
-> RBAC Authorization
-> Sanitized Governed Response
-> Monitoring Metrics + Alert Stream

## API Endpoints
- GET /health
- POST /api/v1/query
- GET /api/v1/metrics
- GET /api/v1/alerts

## Governance Model
- Score range: 0 to 100 from agent confidence and policy penalties.
- Violations tracked: blocked_content, underspecified_query, low_certainty_language.
- RBAC roles:
  - viewer: denied for sensitive queries or low score.
  - analyst: stricter threshold on sensitive queries.
  - admin: can inspect low-score responses, but blocked policy still denies.

## Performance and Monitoring
- Synthetic heterogeneous agent delays simulate real service topology.
- Target behavior: sub-400 ms request latency under default local settings.
- Alerts generated for high latency, low score, and policy violations.

## Tech Stack
- Python 3.11+
- FastAPI
- Pydantic and pydantic-settings
- Pytest and pytest-asyncio
- GitHub Actions CI

## Local Setup
```bash
git clone https://github.com/gnanadeepgudapati/Enterprise-Agent-Governance-Platform.git
cd Enterprise-Agent-Governance-Platform
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run Tests
```bash
pytest
```

## CI/CD
GitHub Actions workflow at .github/workflows/ci.yml runs automated tests on push and pull requests.
