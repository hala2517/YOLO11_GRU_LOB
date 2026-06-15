from app.db.base import Base
from app.models.timestamp import TimestampMixin
from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Dataset(TimestampMixin, Base):
    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    total_images: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    labeled_images: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    storage_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    version: Mapped[str | None] = mapped_column(String(50), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    created_by_user: Mapped["User | None"] = relationship(
        "User", back_populates="datasets", foreign_keys=[created_by]
    )
    training_jobs: Mapped[list["TrainingJob"]] = relationship(
        "TrainingJob", back_populates="dataset", cascade="save-update, merge"
    )
    evaluation_results: Mapped[list["EvaluationResult"]] = relationship(
        "EvaluationResult", back_populates="dataset", cascade="save-update, merge"
    )
    labeling_tasks: Mapped[list["LabelingTask"]] = relationship(
        "LabelingTask", back_populates="dataset", cascade="all, delete-orphan"
    )
    data_collection_jobs: Mapped[list["DataCollectionJob"]] = relationship(
        "DataCollectionJob", back_populates="dataset", cascade="save-update, merge"
    )

    __table_args__ = (
        Index("ix_datasets_name", "name"),
        Index("ix_datasets_is_active", "is_active"),
    )


from app.models.data_collection_job import DataCollectionJob  # noqa: E402
from app.models.evaluation_result import EvaluationResult  # noqa: E402
from app.models.labeling_task import LabelingTask  # noqa: E402
from app.models.training_job import TrainingJob  # noqa: E402
from app.models.user import User  # noqa: E402
