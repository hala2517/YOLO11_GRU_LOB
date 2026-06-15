from decimal import Decimal

from app.db.base import Base
from app.models.timestamp import TimestampMixin
from sqlalchemy import Boolean, ForeignKey, Index, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class LobEbCriteria(TimestampMixin, Base):
    __tablename__ = "lob_eb_criteria"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    site_id: Mapped[int | None] = mapped_column(
        ForeignKey("sites.id", ondelete="SET NULL"), nullable=True
    )
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    line_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    product_code: Mapped[str | None] = mapped_column(String(100), nullable=True)

    lob_target: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    lob_warning: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    eb_target: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    eb_warning: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    takt_time_limit: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    site: Mapped["Site | None"] = relationship("Site")
    created_by_user: Mapped["User | None"] = relationship("User")

    __table_args__ = (
        UniqueConstraint(
            "site_id",
            "line_code",
            "product_code",
            "is_active",
            name="uq_lob_eb_criteria_scope_active",
        ),
        Index("ix_lob_eb_criteria_site_id", "site_id"),
        Index("ix_lob_eb_criteria_line_code", "line_code"),
        Index("ix_lob_eb_criteria_product_code", "product_code"),
        Index("ix_lob_eb_criteria_is_active", "is_active"),
    )


from app.models.site import Site  # noqa: E402
from app.models.user import User  # noqa: E402
