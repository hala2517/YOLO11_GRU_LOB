import datetime as dt
from typing import Annotated

from app.api.deps import get_current_user, get_db_session
from app.models.efficiency_metric import EfficiencyMetric
from app.models.enums import ShiftType
from app.models.user import User
from app.schemas.efficiency_metrics import (
    EfficiencyMetricCreate,
    EfficiencyMetricListResponse,
    EfficiencyMetricResponse,
    EfficiencyMetricUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/efficiency-metrics", tags=["efficiency-metrics"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _get_metric_or_404(metric: EfficiencyMetric | None) -> EfficiencyMetric:
    if metric is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="생산 지표를 찾을 수 없습니다.",
        )
    return metric


@router.post("", response_model=EfficiencyMetricResponse, status_code=status.HTTP_201_CREATED)
async def create_efficiency_metric(
    body: EfficiencyMetricCreate,
    session: DbSession,
    current_user: CurrentUser,
) -> EfficiencyMetric:
    metric = EfficiencyMetric(**body.model_dump())
    session.add(metric)
    await session.commit()
    await session.refresh(metric)
    return metric


@router.get("", response_model=EfficiencyMetricListResponse)
async def list_efficiency_metrics(
    session: DbSession,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    process_id: int | None = Query(default=None),
    shift: ShiftType | None = Query(default=None),
    date_from: dt.date | None = Query(default=None),
    date_to: dt.date | None = Query(default=None),
) -> EfficiencyMetricListResponse:
    conditions = []
    if process_id is not None:
        conditions.append(EfficiencyMetric.process_id == process_id)
    if shift is not None:
        conditions.append(EfficiencyMetric.shift == shift)
    if date_from is not None:
        conditions.append(EfficiencyMetric.date >= date_from)
    if date_to is not None:
        conditions.append(EfficiencyMetric.date <= date_to)

    total = (
        await session.execute(
            select(func.count()).select_from(EfficiencyMetric).where(*conditions)
        )
    ).scalar_one()

    offset = (page - 1) * size
    rows = (
        await session.execute(
            select(EfficiencyMetric)
            .where(*conditions)
            .order_by(EfficiencyMetric.date.desc(), EfficiencyMetric.id.desc())
            .offset(offset)
            .limit(size)
        )
    ).scalars().all()

    return EfficiencyMetricListResponse(
        items=[EfficiencyMetricResponse.model_validate(m) for m in rows],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{metric_id}", response_model=EfficiencyMetricResponse)
async def get_efficiency_metric(
    metric_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> EfficiencyMetric:
    result = await session.execute(
        select(EfficiencyMetric).where(EfficiencyMetric.id == metric_id)
    )
    return _get_metric_or_404(result.scalar_one_or_none())


@router.put("/{metric_id}", response_model=EfficiencyMetricResponse)
async def update_efficiency_metric(
    metric_id: int,
    body: EfficiencyMetricUpdate,
    session: DbSession,
    current_user: CurrentUser,
) -> EfficiencyMetric:
    result = await session.execute(
        select(EfficiencyMetric).where(EfficiencyMetric.id == metric_id)
    )
    metric = _get_metric_or_404(result.scalar_one_or_none())

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(metric, field, value)

    await session.commit()
    await session.refresh(metric)
    return metric


@router.delete("/{metric_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_efficiency_metric(
    metric_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> None:
    result = await session.execute(
        select(EfficiencyMetric).where(EfficiencyMetric.id == metric_id)
    )
    metric = _get_metric_or_404(result.scalar_one_or_none())
    await session.delete(metric)
    await session.commit()
