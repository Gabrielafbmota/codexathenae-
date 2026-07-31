from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(tags=["health"])


@router.get("/health/live", summary="Liveness probe")
async def health_live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ready", summary="Readiness probe")
async def health_ready(request: Request) -> JSONResponse:
    mongo_ok = False
    try:
        client: Any = request.app.state.mongo_client
        await client.admin.command("ping")
        mongo_ok = True
    except Exception:
        pass

    payload: dict[str, Any] = {
        "status": "ok" if mongo_ok else "degraded",
        "checks": {"mongodb": "ok" if mongo_ok else "error"},
    }
    status_code = 200 if mongo_ok else 503
    return JSONResponse(content=payload, status_code=status_code)
