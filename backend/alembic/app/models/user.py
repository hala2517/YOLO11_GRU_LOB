from datetime import datetime

from app.db.base import Base
from app.models.timestamp import TimestampMixin
from sqlalchemy import Boolean, DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    password_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    created_alert_thresholds: Mapped[list["AlertThreshold"]] = relationship(
        "AlertThreshold",
        back_populates="created_by_user",
        foreign_keys="AlertThreshold.created_by",
    )
    acknowledged_alert_logs: Mapped[list["AlertLog"]] = relationship(
        "AlertLog",
        back_populates="acknowledged_by_user",
        foreign_keys="AlertLog.acknowledged_by",
    )
    user_roles: Mapped[list["UserRole"]] = relationship(
        "UserRole", back_populates="user", cascade="all, delete-orphan"
    )
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="user_roles",
        viewonly=True,
        lazy="selectin",
    )
    datasets: Mapped[list["Dataset"]] = relationship(
        "Dataset", back_populates="created_by_user", foreign_keys="Dataset.created_by"
    )
    training_jobs: Mapped[list["TrainingJob"]] = relationship(
        "TrainingJob", back_populates="created_by_user", foreign_keys="TrainingJob.created_by"
    )
    assigned_labeling_tasks: Mapped[list["LabelingTask"]] = relationship(
        "LabelingTask", back_populates="assigned_to_user", foreign_keys="LabelingTask.assigned_to"
    )
    created_labeling_tasks: Mapped[list["LabelingTask"]] = relationship(
        "LabelingTask", back_populates="created_by_user", foreign_keys="LabelingTask.created_by"
    )
    annotations: Mapped[list["Annotation"]] = relationship(
        "Annotation", back_populates="created_by_user", foreign_keys="Annotation.created_by"
    )
    data_collection_jobs: Mapped[list["DataCollectionJob"]] = relationship(
        "DataCollectionJob", back_populates="created_by_user", foreign_keys="DataCollectionJob.created_by"
    )
    processes: Mapped[list["Process"]] = relationship(
        "Process", back_populates="created_by_user", foreign_keys="Process.created_by"
    )
    process_flows: Mapped[list["ProcessFlow"]] = relationship(
        "ProcessFlow", back_populates="created_by_user", foreign_keys="ProcessFlow.created_by"
    )

    __table_args__ = (
        Index("ix_users_login_id", "login_id"),
        Index("ix_users_email", "email"),
        Index("ix_users_is_deleted", "is_deleted"),
    )


from app.models.alert import AlertLog, AlertThreshold  # noqa: E402
from app.models.annotation import Annotation  # noqa: E402
from app.models.data_collection_job import DataCollectionJob  # noqa: E402
from app.models.dataset import Dataset  # noqa: E402
from app.models.labeling_task import LabelingTask  # noqa: E402
from app.models.process import Process  # noqa: E402
from app.models.process_flow import ProcessFlow  # noqa: E402
from app.models.role import Role  # noqa: E402
from app.models.training_job import TrainingJob  # noqa: E402
from app.models.user_role import UserRole  # noqa: E402
