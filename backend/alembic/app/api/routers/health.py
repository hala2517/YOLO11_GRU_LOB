from app.core.config import get_settings
from app.schemas.health import HealthCheck
from fastapi import APIRouter

router = APIRouter()


@router.get("/health", response_model=HealthCheck)
async def health_check() -> HealthCheck:
    settings = get_settings()
    return HealthCheck(
        status="ok",
        environment=settings.app_env,
        app_name=settings.app_name,
        version=settings.app_version,
    )
