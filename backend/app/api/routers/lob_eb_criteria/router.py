from typing import Annotated

from app.api.deps import get_current_user, get_db_session
from app.models.lob_eb_criteria import LobEbCriteria
from app.models.user import User
from app.schemas.lob_eb_criteria import (
    LobEbCriteriaCreate,
    LobEbCriteriaListResponse,
    LobEbCriteriaResponse,
    LobEbCriteriaUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/lob-eb-criteria", tags=["lob-eb-criteria"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _get_criteria_or_404(criteria: LobEbCriteria | None) -> LobEbCriteria:
    if criteria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LOB/EB 기준을 찾을 수 없습니다.",
        )
    return criteria


@router.post("", response_model=LobEbCriteriaResponse, status_code=status.HTTP_201_CREATED)
async def create_lob_eb_criteria(
    body: LobEbCriteriaCreate,
    session: DbSession,
    current_user: CurrentUser,
) -> LobEbCriteria:
    data = body.model_dump()
    data["created_by"] = current_user.id
    criteria = LobEbCriteria(**data)
    session.add(criteria)
    await session.commit()
    await session.refresh(criteria)
    return criteria


@router.get("", response_model=LobEbCriteriaListResponse)
async def list_lob_eb_criteria(
    session: DbSession,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    site_id: int | None = Query(default=None),
    line_code: str | None = Query(default=None),
    product_code: str | None = Query(default=None),
    is_active: bool | None = Query(default=True),
) -> LobEbCriteriaListResponse:
    conditions = []
    if site_id is not None:
        conditions.append(LobEbCriteria.site_id == site_id)
    if line_code is not None:
        conditions.append(LobEbCriteria.line_code == line_code)
    if product_code is not None:
        conditions.append(LobEbCriteria.product_code == product_code)
    if is_active is not None:
        conditions.append(LobEbCriteria.is_active.is_(is_active))

    total = (
        await session.execute(
            select(func.count()).select_from(LobEbCriteria).where(*conditions)
        )
    ).scalar_one()

    offset = (page - 1) * size
    rows = (
        await session.execute(
            select(LobEbCriteria)
            .where(*conditions)
            .order_by(LobEbCriteria.updated_at.desc(), LobEbCriteria.id.desc())
            .offset(offset)
            .limit(size)
        )
    ).scalars().all()

    return LobEbCriteriaListResponse(
        items=[LobEbCriteriaResponse.model_validate(row) for row in rows],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{criteria_id}", response_model=LobEbCriteriaResponse)
async def get_lob_eb_criteria(
    criteria_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> LobEbCriteria:
    result = await session.execute(
        select(LobEbCriteria).where(LobEbCriteria.id == criteria_id)
    )
    return _get_criteria_or_404(result.scalar_one_or_none())


@router.put("/{criteria_id}", response_model=LobEbCriteriaResponse)
async def update_lob_eb_criteria(
    criteria_id: int,
    body: LobEbCriteriaUpdate,
    session: DbSession,
    current_user: CurrentUser,
) -> LobEbCriteria:
    result = await session.execute(
        select(LobEbCriteria).where(LobEbCriteria.id == criteria_id)
    )
    criteria = _get_criteria_or_404(result.scalar_one_or_none())

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(criteria, field, value)

    await session.commit()
    await session.refresh(criteria)
    return criteria


@router.delete("/{criteria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lob_eb_criteria(
    criteria_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> None:
    result = await session.execute(
        select(LobEbCriteria).where(LobEbCriteria.id == criteria_id)
    )
    criteria = _get_criteria_or_404(result.scalar_one_or_none())
    criteria.is_active = False
    await session.commit()
