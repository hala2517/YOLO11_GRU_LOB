from typing import Annotated

from app.api.deps import get_current_user, get_db_session
from app.models.annotation import Annotation
from app.models.user import User
from app.schemas.annotations import (
    AnnotationBulkCreate,
    AnnotationCreate,
    AnnotationListResponse,
    AnnotationResponse,
    ImageWithLabelsResponse,
    LabelItem,
)
from app.schemas.annotations.update import AnnotationUpdate
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

annotations_router = APIRouter(prefix="/annotations", tags=["annotations"])
images_router = APIRouter(prefix="/images", tags=["images"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _get_annotation_or_404(annotation: Annotation | None) -> Annotation:
    if annotation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="어노테이션을 찾을 수 없습니다.",
        )
    return annotation


@annotations_router.post(
    "",
    response_model=list[AnnotationResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_annotations(
    body: AnnotationBulkCreate | AnnotationCreate,
    session: DbSession,
    current_user: CurrentUser,
) -> list[Annotation]:
    if isinstance(body, AnnotationCreate):
        items = [body]
    else:
        items = body.items

    created: list[Annotation] = []
    for item in items:
        annotation = Annotation(**item.model_dump())
        session.add(annotation)
        created.append(annotation)

    await session.commit()
    for ann in created:
        await session.refresh(ann)

    return created


@annotations_router.get("", response_model=AnnotationListResponse)
async def list_annotations(
    session: DbSession,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    labeling_task_id: int | None = Query(default=None),
    image_path: str | None = Query(default=None),
) -> AnnotationListResponse:
    conditions = [Annotation.is_deleted.is_(False)]
    if labeling_task_id is not None:
        conditions.append(Annotation.labeling_task_id == labeling_task_id)
    if image_path is not None:
        conditions.append(Annotation.image_path == image_path)

    total_result = await session.execute(
        select(func.count()).select_from(Annotation).where(*conditions)
    )
    total = total_result.scalar_one()

    offset = (page - 1) * size
    result = await session.execute(
        select(Annotation)
        .where(*conditions)
        .order_by(Annotation.id.asc())
        .offset(offset)
        .limit(size)
    )
    annotations = result.scalars().all()

    return AnnotationListResponse(
        items=[AnnotationResponse.model_validate(a) for a in annotations],
        total=total,
        page=page,
        size=size,
    )


@annotations_router.get("/{annotation_id}", response_model=AnnotationResponse)
async def get_annotation(
    annotation_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> Annotation:
    result = await session.execute(
        select(Annotation).where(
            Annotation.id == annotation_id,
            Annotation.is_deleted.is_(False),
        )
    )
    return _get_annotation_or_404(result.scalar_one_or_none())


@annotations_router.put("/{annotation_id}", response_model=AnnotationResponse)
async def update_annotation(
    annotation_id: int,
    body: AnnotationUpdate,
    session: DbSession,
    current_user: CurrentUser,
) -> Annotation:
    result = await session.execute(
        select(Annotation).where(
            Annotation.id == annotation_id,
            Annotation.is_deleted.is_(False),
        )
    )
    annotation = _get_annotation_or_404(result.scalar_one_or_none())

    update_data = body.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(annotation, field, value)

    await session.commit()
    await session.refresh(annotation)
    return annotation


@annotations_router.delete("/{annotation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_annotation(
    annotation_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> None:
    result = await session.execute(
        select(Annotation).where(
            Annotation.id == annotation_id,
            Annotation.is_deleted.is_(False),
        )
    )
    annotation = _get_annotation_or_404(result.scalar_one_or_none())
    annotation.is_deleted = True
    await session.commit()


@images_router.get("/{image_path:path}/with-labels", response_model=ImageWithLabelsResponse)
async def get_image_with_labels(
    image_path: str,
    session: DbSession,
    current_user: CurrentUser,
    labeling_task_id: int | None = Query(default=None),
) -> ImageWithLabelsResponse:
    conditions = [
        Annotation.image_path == image_path,
        Annotation.is_deleted.is_(False),
    ]
    if labeling_task_id is not None:
        conditions.append(Annotation.labeling_task_id == labeling_task_id)

    result = await session.execute(
        select(Annotation).where(*conditions).order_by(Annotation.id.asc())
    )
    annotations = result.scalars().all()

    labels = [
        LabelItem(
            label_id=a.id,
            class_id=a.class_id,
            class_name=a.class_name,
            bbox=[
                float(a.bbox_x),
                float(a.bbox_y),
                float(a.bbox_width),
                float(a.bbox_height),
            ],
            confidence=float(a.confidence) if a.confidence is not None else None,
        )
        for a in annotations
    ]

    image_url = f"/static/images/{image_path}"

    return ImageWithLabelsResponse(
        image_id=image_path,
        image_url=image_url,
        width=None,
        height=None,
        labels=labels,
    )
