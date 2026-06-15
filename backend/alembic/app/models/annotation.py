from decimal import Decimal

from app.db.base import Base
from app.models.timestamp import TimestampMixin
from sqlalchemy import Boolean, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Annotation(TimestampMixin, Base):
    __tablename__ = "annotations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    labeling_task_id: Mapped[int] = mapped_column(
        ForeignKey("labeling_tasks.id", ondelete="CASCADE"), nullable=False
    )

    image_path: Mapped[str] = mapped_column(Text, nullable=False)

    class_id: Mapped[int] = mapped_column(Integer, nullable=False)
    class_name: Mapped[str] = mapped_column(String(100), nullable=False)

    bbox_x: Mapped[Decimal] = mapped_column(Numeric(8, 6), nullable=False)
    bbox_y: Mapped[Decimal] = mapped_column(Numeric(8, 6), nullable=False)
    bbox_width: Mapped[Decimal] = mapped_column(Numeric(8, 6), nullable=False)
    bbox_height: Mapped[Decimal] = mapped_column(Numeric(8, 6), nullable=False)

    confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    labeling_task: Mapped["LabelingTask"] = relationship(
        "LabelingTask", back_populates="annotations"
    )
    created_by_user: Mapped["User | None"] = relationship(
        "User", back_populates="annotations", foreign_keys=[created_by]
    )

    __table_args__ = (
        Index("ix_annotations_labeling_task_id", "labeling_task_id"),
        Index("ix_annotations_image_path", "image_path"),
        Index("ix_annotations_class_id", "class_id"),
        Index("ix_annotations_is_deleted", "is_deleted"),
    )


from app.models.labeling_task import LabelingTask  # noqa: E402
from app.models.user import User  # noqa: E402
