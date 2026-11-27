"""Agent service entry point.

Sprint 0: health only. Sprint 1 adds the LLM router and the Requirement agent;
Sprint 3 adds the LangGraph supervisor (see docs/03-architecture/LLD.md).
"""

from fastapi import FastAPI

from app.config import get_settings

app = FastAPI(title="TalentScout Agent Service", version="0.1.0", docs_url="/docs")


@app.get("/health")
def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": "agents",
        "env": settings.env,
        "local_model": settings.local_model,
    }
