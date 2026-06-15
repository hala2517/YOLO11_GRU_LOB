from datetime import datetime, timezone
from typing import Annotated

from app.api.deps import get_db_session
from app.models.dataset import Dataset
from app.models.enums import TrainingJobStatus
from app.models.training_job import TrainingJob
from app.schemas.training_jobs import (
    TrainingJobCreate,
    TrainingJobListResponse,
    TrainingJobResponse,
    TrainingJobUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/training-jobs", tags=["training-jobs"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


def _get_job_or_404(job: TrainingJob | None) -> TrainingJob:
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="학습 작업을 찾을 수 없습니다.",
        )
    return job


@router.post("", response_model=TrainingJobResponse, status_code=status.HTTP_201_CREATED)
async def create_training_job(body: TrainingJobCreate, session: DbSession) -> TrainingJob:
    # Verify dataset exists
    dataset_result = await session.execute(
        select(Dataset).where(Dataset.id == body.dataset_id, Dataset.is_active.is_(True))
    )
    if dataset_result.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="데이터셋을 찾을 수 없습니다.",
        )

    job = TrainingJob(
        job_name=body.job_name,
        dataset_id=body.dataset_id,
        model_id=body.model_id,
        parameters=body.parameters,
        external_job_id=body.external_job_id,
        source_system=body.source_system,
        created_by=body.created_by,
    )
    session.add(job)
    await session.commit()
    await session.refresh(job)
    return job


@router.get("", response_model=TrainingJobListResponse)
async def list_training_jobs(
    session: DbSession,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    status: TrainingJobStatus | None = Query(default=None),
) -> TrainingJobListResponse:
    conditions = []
    if status is not None:
        conditions.append(TrainingJob.status == status)

    total_result = await session.execute(
        select(func.count()).select_from(TrainingJob).where(*conditions)
    )
    total = total_result.scalar_one()

    offset = (page - 1) * size
    result = await session.execute(
        select(TrainingJob)
        .where(*conditions)
        .order_by(TrainingJob.id.desc())
        .offset(offset)
        .limit(size)
    )
    jobs = result.scalars().all()

    return TrainingJobListResponse(
        items=[TrainingJobResponse.model_validate(j) for j in jobs],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{job_id}", response_model=TrainingJobResponse)
async def get_training_job(job_id: int, session: DbSession) -> TrainingJob:
    result = await session.execute(
        select(TrainingJob).where(TrainingJob.id == job_id)
    )
    return _get_job_or_404(result.scalar_one_or_none())


@router.patch("/{job_id}", response_model=TrainingJobResponse)
async def update_training_job(
    job_id: int,
    body: TrainingJobUpdate,
    session: DbSession,
) -> TrainingJob:
    result = await session.execute(
        select(TrainingJob).where(TrainingJob.id == job_id)
    )
    job = _get_job_or_404(result.scalar_one_or_none())

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(job, field, value)

    await session.commit()
    await session.refresh(job)
    return job


@router.put("/{job_id}/cancel", response_model=TrainingJobResponse)
async def cancel_training_job(job_id: int, session: DbSession) -> TrainingJob:
    result = await session.execute(
        select(TrainingJob).where(TrainingJob.id == job_id)
    )
    job = _get_job_or_404(result.scalar_one_or_none())

    if job.status not in (TrainingJobStatus.pending, TrainingJobStatus.running):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="진행 중이거나 대기 중인 작업만 취소할 수 있습니다.",
        )

    job.status = TrainingJobStatus.cancelled
    job.completed_at = datetime.now(timezone.utc)
    await session.commit()
    await session.refresh(job)
    return job
