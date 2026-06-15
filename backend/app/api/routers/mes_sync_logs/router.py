from datetime import datetime, timezone
from typing import Annotated

from app.api.deps import get_current_user, get_db_session
from app.models.enums import MesSyncStatus
from app.models.mes_sync_log import MesSyncLog
from app.models.user import User
from app.schemas.mes_sync_logs import (
    MesSyncLogCreate,
    MesSyncLogListResponse,
    MesSyncLogResponse,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/mes-sync-logs", tags=["mes-sync-logs"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _get_log_or_404(log: MesSyncLog | None) -> MesSyncLog:
    if log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MES 동기화 로그를 찾을 수 없습니다.",
        )
    return log


@router.post("", response_model=MesSyncLogResponse, status_code=status.HTTP_201_CREATED)
async def create_mes_sync_log(
    body: MesSyncLogCreate,
    session: DbSession,
    current_user: CurrentUser,
) -> MesSyncLog:
    log = MesSyncLog(
        site_id=body.site_id,
        payload=body.payload,
        processed_status=body.processed_status,
    )
    session.add(log)
    await session.commit()
    await session.refresh(log)
    return log


@router.get("", response_model=MesSyncLogListResponse)
async def list_mes_sync_logs(
    session: DbSession,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    site_id: int | None = Query(default=None),
    processed_status: MesSyncStatus | None = Query(default=None),
) -> MesSyncLogListResponse:
    conditions = []
    if site_id is not None:
        conditions.append(MesSyncLog.site_id == site_id)
    if processed_status is not None:
        conditions.append(MesSyncLog.processed_status == processed_status)

    total = (
        await session.execute(
            select(func.count()).select_from(MesSyncLog).where(*conditions)
        )
    ).scalar_one()

    offset = (page - 1) * size
    rows = (
        await session.execute(
            select(MesSyncLog)
            .where(*conditions)
            .order_by(MesSyncLog.created_at.desc())
            .offset(offset)
            .limit(size)
        )
    ).scalars().all()

    return MesSyncLogListResponse(
        items=[MesSyncLogResponse.model_validate(r) for r in rows],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{log_id}", response_model=MesSyncLogResponse)
async def get_mes_sync_log(
    log_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> MesSyncLog:
    result = await session.execute(
        select(MesSyncLog).where(MesSyncLog.id == log_id)
    )
    return _get_log_or_404(result.scalar_one_or_none())


@router.patch("/{log_id}/status", response_model=MesSyncLogResponse)
async def update_mes_sync_status(
    log_id: int,
    processed_status: MesSyncStatus,
    error_message: str | None,
    session: DbSession,
    current_user: CurrentUser,
) -> MesSyncLog:
    result = await session.execute(
        select(MesSyncLog).where(MesSyncLog.id == log_id)
    )
    log = _get_log_or_404(result.scalar_one_or_none())

    log.processed_status = processed_status
    log.error_message = error_message
    if processed_status in (MesSyncStatus.success, MesSyncStatus.failed):
        log.processed_at = datetime.now(timezone.utc)

    await session.commit()
    await session.refresh(log)
    return log
