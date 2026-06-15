from app.db.base import Base
from app.models.enums import AIModelType
from app.models.timestamp import TimestampMixin
from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, Index, Numeric, String, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AIModel(TimestampMixin, Base):
    __tablename__ = "ai_models"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    model_type: Mapped[AIModelType] = mapped_column(
        Enum(AIModelType, name="ai_model_type"), nullable=False
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    file_size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    mAP: Mapped[Decimal | None] = mapped_column(Numeric(6, 4), nullable=True)
    precision: Mapped[Decimal | None] = mapped_column(Numeric(6, 4), nullable=True)
    recall: Mapped[Decimal | None] = mapped_column(Numeric(6, 4), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_deployed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    trained_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    training_jobs: Mapped[list["TrainingJob"]] = relationship(
        "TrainingJob", back_populates="model", cascade="save-update, merge"
    )
    evaluation_results: Mapped[list["EvaluationResult"]] = relationship(
        "EvaluationResult", back_populates="model", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_ai_models_model_type", "model_type"),
        Index("ix_ai_models_is_active", "is_active"),
    )


_SEED_MODELS = [
    {"name": "객체인식 모델", "model_type": AIModelType.detection, "version": "v1.0"},
    {"name": "행동인식 모델", "model_type": AIModelType.action_detection, "version": "v1.0"},
    {"name": "행동분류 모델", "model_type": AIModelType.action_classification, "version": "v1.0"},
]


async def seed_ai_models(session: AsyncSession) -> None:
    from sqlalchemy import select

    for data in _SEED_MODELS:
        result = await session.execute(
            select(AIModel).where(AIModel.name == data["name"])
        )
        if result.scalar_one_or_none() is None:
            session.add(AIModel(**data))

    await session.commit()


from app.models.evaluation_result import EvaluationResult  # noqa: E402
from app.models.training_job import TrainingJob  # noqa: E402
