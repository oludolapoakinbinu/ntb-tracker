from fastapi import FastAPI

from app import __version__
from app.api.router import api_router
from app.core.config import get_settings

DESCRIPTION = """
github project
"""


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description=DESCRIPTION,
    )
    app.include_router(api_router)
    return app


app = create_app()
