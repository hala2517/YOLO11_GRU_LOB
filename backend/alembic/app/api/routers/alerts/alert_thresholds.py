from typing import Annotated

from app.api.deps import get_db_session
from app.models.alert import AlertThreshold
from app.schemas.alert import (
    AlertThresholdCreate,
    AlertThresholdListResponse,
    AlertThresholdResponse,
    AlertThresholdUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/alert-thresholds", tags=["alert-thresholds"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


def _get_threshold_or_404(threshold: AlertThreshold | None) -> AlertThreshold:
    if threshold is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="알림 임계값을 찾을 수 없습니다.",
        )
    return threshold


@router.post("", response_model=AlertThresholdResponse, status_code=status.HTTP_201_CREATED)
async def create_threshold(body: AlertThresholdCreate, session: DbSession) -> AlertThreshold:
    threshold = AlertThreshold(**body.model_dump())
    session.add(threshold)
    await session.commit()
    await session.refresh(threshold)
    return threshold


@router.get("", response_model=AlertThresholdListResponse)
async def list_thresholds(
    session: DbSession,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    site_id: int | None = Query(default=None),
    is_active: bool | None = Query(default=None),
) -> AlertThresholdListResponse:
    conditions = []
    if site_id is not None:
        conditions.append(AlertThreshold.site_id == site_id)
    if is_active is not None:
        conditions.append(AlertThreshold.is_active.is_(is_active))

    base_query = select(AlertThreshold).where(*conditions)
    total_result = await session.execute(
        select(func.count()).select_from(AlertThreshold).where(*conditions)
    )
    total = total_result.scalar_one()

    offset = (page - 1) * size
    result = await session.execute(
        base_query.order_by(AlertThreshold.id.asc()).offset(offset).limit(size)
    )
    thresholds = result.scalars().all()

    return AlertThresholdListResponse(
        items=[AlertThresholdResponse.model_validate(t) for t in thresholds],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{threshold_id}", response_model=AlertThresholdResponse)
async def get_threshold(threshold_id: int, session: DbSession) -> AlertThreshold:
    result = await session.execute(
        select(AlertThreshold).where(AlertThreshold.id == threshold_id)
    )
    return _get_threshold_or_404(result.scalar_one_or_none())


@router.put("/{threshold_id}", response_model=AlertThresholdResponse)
async def update_threshold(
    threshold_id: int, body: AlertThresholdUpdate, session: DbSession
) -> AlertThreshold:
    result = await session.execute(
        select(AlertThreshold).where(AlertThreshold.id == threshold_id)
    )
    threshold = _get_threshold_or_404(result.scalar_one_or_none())

    update_data = body.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(threshold, field, value)

    await session.commit()
    await session.refresh(threshold)
    return threshold


@router.delete("/{threshold_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_threshold(threshold_id: int, session: DbSession) -> None:
    result = await session.execute(
        select(AlertThreshold).where(AlertThreshold.id == threshold_id)
    )
    threshold = _get_threshold_or_404(result.scalar_one_or_none())
    threshold.is_active = False
    await session.commit()
