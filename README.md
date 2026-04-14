# Enterprise Agent Governance Platform

A production-grade multi-agent orchestration platform with Safe AI validation, 
governance, and audit trail — built to demonstrate enterprise-ready AI agent architecture.

## What This Does
A user asks a complex enterprise question. Instead of one AI answering it, 
three specialized agents collaborate:
- **Knowledge Agent** — retrieves relevant information using RAG
- **Compliance Agent** — checks if the answer is safe and policy-compliant
- **Synthesis Agent** — produces the final governed response

Every answer passes through a Safe AI layer and is logged to an audit trail.

## Architecture
User Query → Orchestrator → [Knowledge | Compliance | Synthesis] Agents
↓
Safe AI Layer (hallucination + toxicity check)
↓
Governance Bus (audit log + RBAC)
↓
Final Response

## Tech Stack
- **FastAPI** — API framework
- **Pydantic** — data validation
- **Groq** — LLM inference for agents
- **PostgreSQL** — audit trail storage
- **Docker** — containerized deployment

## Getting Started
git clone https://github.com/gnanadeepgudapati/Enterprise-Agent-Governance-Platform.git
cd Enterprise-Agent-Governance-Platform
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

## Running Tests
pytest

## Project Status
🚧 Active development — Week 1 of 6
