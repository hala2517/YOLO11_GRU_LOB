from typing import Annotated

from app.api.deps import get_db_session
from app.models.role import Role
from app.schemas.roles import RoleListResponse, RoleResponse
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/roles", tags=["roles"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


@router.get("", response_model=RoleListResponse)
async def list_roles(
    session: DbSession,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    is_active: bool | None = Query(default=None),
) -> RoleListResponse:
    conditions = []
    if is_active is not None:
        conditions.append(Role.is_active.is_(is_active))

    total_result = await session.execute(
        select(func.count()).select_from(Role).where(*conditions)
    )
    total = total_result.scalar_one()

    offset = (page - 1) * size
    result = await session.execute(
        select(Role).where(*conditions).order_by(Role.id.asc()).offset(offset).limit(size)
    )
    roles = result.scalars().all()

    return RoleListResponse(
        items=[RoleResponse.model_validate(r) for r in roles],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int, session: DbSession) -> Role:
    result = await session.execute(
        select(Role).where(Role.id == role_id)
    )
    role = result.scalar_one_or_none()
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="역할을 찾을 수 없습니다.",
        )
    return role
