from typing import Annotated

from app.api.deps import get_current_user, get_db_session
from app.models.process import Process
from app.models.process_flow import ProcessFlow
from app.models.user import User
from app.schemas.process_flows import (
    ProcessFlowCreate,
    ProcessFlowListResponse,
    ProcessFlowResponse,
    ProcessFlowUpdate,
)
from app.schemas.processes import (
    ProcessCreate,
    ProcessListResponse,
    ProcessResponse,
    ProcessUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/processes", tags=["processes"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _get_process_or_404(process: Process | None) -> Process:
    if process is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="공정을 찾을 수 없습니다.",
        )
    return process


def _get_flow_or_404(flow: ProcessFlow | None) -> ProcessFlow:
    if flow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="공정 흐름도를 찾을 수 없습니다.",
        )
    return flow


@router.post("", response_model=ProcessResponse, status_code=status.HTTP_201_CREATED)
async def create_process(
    body: ProcessCreate,
    session: DbSession,
    current_user: CurrentUser,
) -> Process:
    if body.code:
        dup = await session.execute(
            select(Process).where(
                Process.site_id == body.site_id,
                Process.code == body.code,
                Process.is_deleted.is_(False),
            )
        )
        if dup.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="해당 사이트에 이미 동일한 공정 코드가 존재합니다.",
            )
    process = Process(**body.model_dump())
    session.add(process)
    await session.commit()
    await session.refresh(process)
    return process


@router.get("", response_model=ProcessListResponse)
async def list_processes(
    session: DbSession,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    site_id: int | None = Query(default=None),
    is_active: bool | None = Query(default=None),
) -> ProcessListResponse:
    conditions = [Process.is_deleted.is_(False)]
    if site_id is not None:
        conditions.append(Process.site_id == site_id)
    if is_active is not None:
        conditions.append(Process.is_active.is_(is_active))

    total = (
        await session.execute(
            select(func.count()).select_from(Process).where(*conditions)
        )
    ).scalar_one()

    offset = (page - 1) * size
    rows = (
        await session.execute(
            select(Process)
            .where(*conditions)
            .order_by(Process.site_id.asc(), Process.line_order.asc(), Process.id.asc())
            .offset(offset)
            .limit(size)
        )
    ).scalars().all()

    return ProcessListResponse(
        items=[ProcessResponse.model_validate(p) for p in rows],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{process_id}", response_model=ProcessResponse)
async def get_process(
    process_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> Process:
    result = await session.execute(
        select(Process).where(Process.id == process_id, Process.is_deleted.is_(False))
    )
    return _get_process_or_404(result.scalar_one_or_none())


@router.put("/{process_id}", response_model=ProcessResponse)
async def update_process(
    process_id: int,
    body: ProcessUpdate,
    session: DbSession,
    current_user: CurrentUser,
) -> Process:
    result = await session.execute(
        select(Process).where(Process.id == process_id, Process.is_deleted.is_(False))
    )
    process = _get_process_or_404(result.scalar_one_or_none())

    if body.code and body.code != process.code:
        dup = await session.execute(
            select(Process).where(
                Process.site_id == process.site_id,
                Process.code == body.code,
                Process.is_deleted.is_(False),
                Process.id != process_id,
            )
        )
        if dup.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="해당 사이트에 이미 동일한 공정 코드가 존재합니다.",
            )

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(process, field, value)

    await session.commit()
    await session.refresh(process)
    return process


@router.delete("/{process_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_process(
    process_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> None:
    result = await session.execute(
        select(Process).where(Process.id == process_id, Process.is_deleted.is_(False))
    )
    process = _get_process_or_404(result.scalar_one_or_none())
    process.is_deleted = True
    await session.commit()


@router.post(
    "/{process_id}/flows",
    response_model=ProcessFlowResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_process_flow(
    process_id: int,
    body: ProcessFlowCreate,
    session: DbSession,
    current_user: CurrentUser,
) -> ProcessFlow:
    result = await session.execute(
        select(Process).where(Process.id == process_id, Process.is_deleted.is_(False))
    )
    _get_process_or_404(result.scalar_one_or_none())

    dup = await session.execute(
        select(ProcessFlow).where(
            ProcessFlow.process_id == process_id,
            ProcessFlow.version == body.version,
            ProcessFlow.is_deleted.is_(False),
        )
    )
    if dup.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"버전 {body.version}이 이미 존재합니다.",
        )

    data = body.model_dump()
    data["process_id"] = process_id
    flow = ProcessFlow(**data)
    session.add(flow)
    await session.commit()
    await session.refresh(flow)
    return flow


@router.get("/{process_id}/flows", response_model=ProcessFlowListResponse)
async def list_process_flows(
    process_id: int,
    session: DbSession,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    is_active: bool | None = Query(default=None),
) -> ProcessFlowListResponse:
    result = await session.execute(
        select(Process).where(Process.id == process_id, Process.is_deleted.is_(False))
    )
    _get_process_or_404(result.scalar_one_or_none())

    conditions = [
        ProcessFlow.process_id == process_id,
        ProcessFlow.is_deleted.is_(False),
    ]
    if is_active is not None:
        conditions.append(ProcessFlow.is_active.is_(is_active))

    total = (
        await session.execute(
            select(func.count()).select_from(ProcessFlow).where(*conditions)
        )
    ).scalar_one()

    offset = (page - 1) * size
    rows = (
        await session.execute(
            select(ProcessFlow)
            .where(*conditions)
            .order_by(ProcessFlow.version.desc())
            .offset(offset)
            .limit(size)
        )
    ).scalars().all()

    return ProcessFlowListResponse(
        items=[ProcessFlowResponse.model_validate(f) for f in rows],
        total=total,
        page=page,
        size=size,
    )


@router.put("/{process_id}/flows/{flow_id}", response_model=ProcessFlowResponse)
async def update_process_flow(
    process_id: int,
    flow_id: int,
    body: ProcessFlowUpdate,
    session: DbSession,
    current_user: CurrentUser,
) -> ProcessFlow:
    result = await session.execute(
        select(ProcessFlow).where(
            ProcessFlow.id == flow_id,
            ProcessFlow.process_id == process_id,
            ProcessFlow.is_deleted.is_(False),
        )
    )
    flow = _get_flow_or_404(result.scalar_one_or_none())

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(flow, field, value)

    await session.commit()
    await session.refresh(flow)
    return flow
