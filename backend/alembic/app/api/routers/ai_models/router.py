from typing import Annotated

from app.api.deps import get_db_session
from app.models.ai_model import AIModel
from app.schemas.ai_models import AIModelListResponse, AIModelResponse
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/ai-models", tags=["ai-models"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


@router.get("", response_model=AIModelListResponse)
async def list_ai_models(
    session: DbSession,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    is_active: bool | None = Query(default=None),
) -> AIModelListResponse:
    conditions = []
    if is_active is not None:
        conditions.append(AIModel.is_active.is_(is_active))

    total_result = await session.execute(
        select(func.count()).select_from(AIModel).where(*conditions)
    )
    total = total_result.scalar_one()

    offset = (page - 1) * size
    result = await session.execute(
        select(AIModel).where(*conditions).order_by(AIModel.id.asc()).offset(offset).limit(size)
    )
    models = result.scalars().all()

    return AIModelListResponse(
        items=[AIModelResponse.model_validate(m) for m in models],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{model_id}", response_model=AIModelResponse)
async def get_ai_model(model_id: int, session: DbSession) -> AIModel:
    result = await session.execute(
        select(AIModel).where(AIModel.id == model_id)
    )
    model = result.scalar_one_or_none()
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI 모델을 찾을 수 없습니다.",
        )
    return model
