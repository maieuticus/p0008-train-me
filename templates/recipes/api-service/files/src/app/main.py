"""Minimal API; business behavior is added through feature specifications."""

from fastapi import FastAPI

app = FastAPI(title="Project API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness only; this endpoint does not assert database readiness."""
    return {"status": "ok"}
