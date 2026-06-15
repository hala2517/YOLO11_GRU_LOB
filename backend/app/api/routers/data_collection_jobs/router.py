from datetime import datetime, timezone
from typing import Annotated

from app.api.deps import get_current_user, get_db_session
from app.models.data_collection_job import DataCollectionJob
from app.models.enums import DataCollectionJobStatus
from app.models.user import User
from app.schemas.data_collection_jobs import (
    DataCollectionJobCreate,
    DataCollectionJobListResponse,
    DataCollectionJobResponse,
    DataCollectionJobUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/data-collection-jobs", tags=["data-collection-jobs"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _get_job_or_404(job: DataCollectionJob | None) -> DataCollectionJob:
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="데이터 수집 작업을 찾을 수 없습니다.",
        )
    return job


@router.post("", response_model=DataCollectionJobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    body: DataCollectionJobCreate,
    session: DbSession,
    current_user: CurrentUser,
) -> DataCollectionJob:
    job = DataCollectionJob(**body.model_dump())
    session.add(job)
    await session.commit()
    await session.refresh(job)
    return job


@router.get("", response_model=DataCollectionJobListResponse)
async def list_jobs(
    session: DbSession,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    camera_id: int | None = Query(default=None),
    status_filter: DataCollectionJobStatus | None = Query(default=None, alias="status"),
) -> DataCollectionJobListResponse:
    conditions = [DataCollectionJob.is_deleted.is_(False)]
    if camera_id is not None:
        conditions.append(DataCollectionJob.camera_id == camera_id)
    if status_filter is not None:
        conditions.append(DataCollectionJob.status == status_filter)

    total_result = await session.execute(
        select(func.count()).select_from(DataCollectionJob).where(*conditions)
    )
    total = total_result.scalar_one()

    offset = (page - 1) * size
    result = await session.execute(
        select(DataCollectionJob)
        .where(*conditions)
        .order_by(DataCollectionJob.id.desc())
        .offset(offset)
        .limit(size)
    )
    jobs = result.scalars().all()

    return DataCollectionJobListResponse(
        items=[DataCollectionJobResponse.model_validate(j) for j in jobs],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{job_id}", response_model=DataCollectionJobResponse)
async def get_job(
    job_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> DataCollectionJob:
    result = await session.execute(
        select(DataCollectionJob).where(
            DataCollectionJob.id == job_id,
            DataCollectionJob.is_deleted.is_(False),
        )
    )
    return _get_job_or_404(result.scalar_one_or_none())


@router.put("/{job_id}", response_model=DataCollectionJobResponse)
async def update_job(
    job_id: int,
    body: DataCollectionJobUpdate,
    session: DbSession,
    current_user: CurrentUser,
) -> DataCollectionJob:
    result = await session.execute(
        select(DataCollectionJob).where(
            DataCollectionJob.id == job_id,
            DataCollectionJob.is_deleted.is_(False),
        )
    )
    job = _get_job_or_404(result.scalar_one_or_none())

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(job, field, value)

    await session.commit()
    await session.refresh(job)
    return job


@router.post("/{job_id}/trigger", response_model=DataCollectionJobResponse)
async def trigger_job(
    job_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> DataCollectionJob:
    result = await session.execute(
        select(DataCollectionJob).where(
            DataCollectionJob.id == job_id,
            DataCollectionJob.is_deleted.is_(False),
        )
    )
    job = _get_job_or_404(result.scalar_one_or_none())

    if job.status == DataCollectionJobStatus.running:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 실행 중인 작업입니다.",
        )

    job.status = DataCollectionJobStatus.running
    job.last_run_at = datetime.now(timezone.utc)
    job.error_message = None

    await session.commit()
    await session.refresh(job)
    return job


@router.post("/{job_id}/cancel", response_model=DataCollectionJobResponse)
async def cancel_job(
    job_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> DataCollectionJob:
    result = await session.execute(
        select(DataCollectionJob).where(
            DataCollectionJob.id == job_id,
            DataCollectionJob.is_deleted.is_(False),
        )
    )
    job = _get_job_or_404(result.scalar_one_or_none())

    if job.status not in (DataCollectionJobStatus.pending, DataCollectionJobStatus.running):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="취소할 수 없는 상태입니다.",
        )

    job.status = DataCollectionJobStatus.cancelled

    await session.commit()
    await session.refresh(job)
    return job
