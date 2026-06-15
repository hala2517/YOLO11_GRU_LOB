from datetime import datetime, timezone
from typing import Annotated

from app.api.deps import get_db_session
from app.models.alert import AlertLog
from app.models.enums import AlertSeverity, AlertType
from app.schemas.alert import AlertLogAcknowledge, AlertLogListResponse, AlertLogResponse
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/alert-logs", tags=["alert-logs"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


def _get_log_or_404(log: AlertLog | None) -> AlertLog:
    if log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="알림 로그를 찾을 수 없습니다.",
        )
    return log


@router.get("", response_model=AlertLogListResponse)
async def list_alert_logs(
    session: DbSession,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    site_id: int | None = Query(default=None),
    alert_type: AlertType | None = Query(default=None),
    severity: AlertSeverity | None = Query(default=None),
    is_acknowledged: bool | None = Query(default=None),
    start_date: datetime | None = Query(default=None),
    end_date: datetime | None = Query(default=None),
) -> AlertLogListResponse:
    conditions = []
    if site_id is not None:
        conditions.append(AlertLog.site_id == site_id)
    if alert_type is not None:
        conditions.append(AlertLog.alert_type == alert_type)
    if severity is not None:
        conditions.append(AlertLog.severity == severity)
    if is_acknowledged is not None:
        conditions.append(AlertLog.is_acknowledged.is_(is_acknowledged))
    if start_date is not None:
        conditions.append(AlertLog.detected_at >= start_date)
    if end_date is not None:
        conditions.append(AlertLog.detected_at <= end_date)

    total_result = await session.execute(
        select(func.count()).select_from(AlertLog).where(*conditions)
    )
    total = total_result.scalar_one()

    offset = (page - 1) * size
    result = await session.execute(
        select(AlertLog)
        .where(*conditions)
        .order_by(AlertLog.detected_at.desc())
        .offset(offset)
        .limit(size)
    )
    logs = result.scalars().all()

    return AlertLogListResponse(
        items=[AlertLogResponse.model_validate(log) for log in logs],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{alert_log_id}", response_model=AlertLogResponse)
async def get_alert_log(alert_log_id: int, session: DbSession) -> AlertLog:
    result = await session.execute(
        select(AlertLog).where(AlertLog.id == alert_log_id)
    )
    return _get_log_or_404(result.scalar_one_or_none())


@router.put("/{alert_log_id}/acknowledge", response_model=AlertLogResponse)
async def acknowledge_alert_log(
    alert_log_id: int, body: AlertLogAcknowledge, session: DbSession
) -> AlertLog:
    result = await session.execute(
        select(AlertLog).where(AlertLog.id == alert_log_id)
    )
    log = _get_log_or_404(result.scalar_one_or_none())

    if log.is_acknowledged:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 확인된 알림입니다.",
        )

    log.is_acknowledged = True
    log.acknowledged_by = body.acknowledged_by
    log.acknowledged_at = datetime.now(timezone.utc)

    await session.commit()
    await session.refresh(log)
    return log
