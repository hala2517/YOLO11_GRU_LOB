from contextlib import asynccontextmanager

from app.api.main import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.session import async_session_factory, engine
from app.models.ai_model import seed_ai_models
from app.models.role import seed_roles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with async_session_factory() as session:
        await seed_roles(session)
        await seed_ai_models(session)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url=f"{settings.api_v1_str}/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_v1_str)

    @app.get("/", tags=["root"])
    async def root() -> dict[str, str]:
        return {"message": settings.app_name}

    return app


app = create_app()
