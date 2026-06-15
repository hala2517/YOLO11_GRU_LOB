from datetime import date, datetime, time, timezone
from typing import Annotated

from app.api.deps import get_db_session
from app.models.evaluation_result import EvaluationResult
from app.schemas.evaluation_results import (
    EvaluationResultCreate,
    EvaluationResultListResponse,
    EvaluationResultResponse,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/evaluation-results", tags=["evaluation-results"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


def _get_result_or_404(result: EvaluationResult | None) -> EvaluationResult:
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="평가 결과를 찾을 수 없습니다.",
        )
    return result


@router.get("", response_model=EvaluationResultListResponse)
async def list_evaluation_results(
    session: DbSession,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    model_id: int | None = Query(default=None),
    dataset_id: int | None = Query(default=None),
    training_job_id: int | None = Query(default=None),
    start_date: date | None = Query(default=None, description="평가 시작일 (YYYY-MM-DD)"),
    end_date: date | None = Query(default=None, description="평가 종료일 (YYYY-MM-DD)"),
) -> EvaluationResultListResponse:
    conditions = []
    if model_id is not None:
        conditions.append(EvaluationResult.model_id == model_id)
    if dataset_id is not None:
        conditions.append(EvaluationResult.dataset_id == dataset_id)
    if training_job_id is not None:
        conditions.append(EvaluationResult.training_job_id == training_job_id)
    if start_date is not None:
        conditions.append(EvaluationResult.evaluation_date >= datetime.combine(start_date, time.min, tzinfo=timezone.utc))
    if end_date is not None:
        conditions.append(EvaluationResult.evaluation_date <= datetime.combine(end_date, time.max, tzinfo=timezone.utc))

    total_result = await session.execute(
        select(func.count()).select_from(EvaluationResult).where(*conditions)
    )
    total = total_result.scalar_one()

    offset = (page - 1) * size
    result = await session.execute(
        select(EvaluationResult)
        .where(*conditions)
        .order_by(EvaluationResult.evaluation_date.desc())
        .offset(offset)
        .limit(size)
    )
    items = result.scalars().all()

    return EvaluationResultListResponse(
        items=[EvaluationResultResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{result_id}", response_model=EvaluationResultResponse)
async def get_evaluation_result(result_id: int, session: DbSession) -> EvaluationResult:
    result = await session.execute(
        select(EvaluationResult).where(EvaluationResult.id == result_id)
    )
    return _get_result_or_404(result.scalar_one_or_none())


@router.post("", response_model=EvaluationResultResponse, status_code=status.HTTP_201_CREATED)
async def create_evaluation_result(
    body: EvaluationResultCreate,
    session: DbSession,
) -> EvaluationResult:
    result = EvaluationResult(**body.model_dump(exclude_none=True))
    session.add(result)
    await session.commit()
    await session.refresh(result)
    return result


@router.post("/scan", status_code=status.HTTP_202_ACCEPTED)
async def scan_evaluation_results(session: DbSession) -> dict[str, str]:
    """
    수동으로 평가 결과 폴더 스캔을 트리거합니다.
    실제 스캔 로직은 백그라운드에서 처리됩니다.
    """
    # TODO: 실제 스캔 로직 구현
    # 현재는 스캔 작업 수락 응답만 반환
    return {"message": "평가 결과 폴더 스캔이 시작되었습니다."}
