from fastapi import APIRouter

from app import __version__
from app.core.config import get_settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["meta"])


@router.get("/health", response_model=HealthResponse, summary="Service health")
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(version=__version__, environment=settings.environment)
