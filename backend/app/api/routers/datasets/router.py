from typing import Annotated

from app.api.deps import get_db_session
from app.models.dataset import Dataset
from app.schemas.datasets import DatasetCreate, DatasetListResponse, DatasetResponse, DatasetUpdate
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/datasets", tags=["datasets"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


def _get_dataset_or_404(dataset: Dataset | None) -> Dataset:
    if dataset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="데이터셋을 찾을 수 없습니다.",
        )
    return dataset


@router.post("", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def create_dataset(body: DatasetCreate, session: DbSession) -> Dataset:
    dataset = Dataset(**body.model_dump())
    session.add(dataset)
    await session.commit()
    await session.refresh(dataset)
    return dataset


@router.get("", response_model=DatasetListResponse)
async def list_datasets(
    session: DbSession,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    is_active: bool | None = Query(default=None),
) -> DatasetListResponse:
    conditions = []
    if is_active is not None:
        conditions.append(Dataset.is_active.is_(is_active))

    total_result = await session.execute(
        select(func.count()).select_from(Dataset).where(*conditions)
    )
    total = total_result.scalar_one()

    offset = (page - 1) * size
    result = await session.execute(
        select(Dataset).where(*conditions).order_by(Dataset.id.desc()).offset(offset).limit(size)
    )
    datasets = result.scalars().all()

    return DatasetListResponse(
        items=[DatasetResponse.model_validate(d) for d in datasets],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(dataset_id: int, session: DbSession) -> Dataset:
    result = await session.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    )
    return _get_dataset_or_404(result.scalar_one_or_none())


@router.put("/{dataset_id}", response_model=DatasetResponse)
async def update_dataset(
    dataset_id: int, body: DatasetUpdate, session: DbSession
) -> Dataset:
    result = await session.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    )
    dataset = _get_dataset_or_404(result.scalar_one_or_none())

    update_data = body.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(dataset, field, value)

    await session.commit()
    await session.refresh(dataset)
    return dataset
