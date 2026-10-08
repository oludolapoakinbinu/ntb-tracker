from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.tbills import router as tbills_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(tbills_router)
