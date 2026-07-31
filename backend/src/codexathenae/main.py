"""Entry point for the CodexAthenae API."""

import uvicorn

from codexathenae.factory import create_app
from codexathenae.infrastructure.settings.config import get_settings

settings = get_settings()
app = create_app(settings)

if __name__ == "__main__":
    uvicorn.run(
        "codexathenae.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_config=None,
    )
