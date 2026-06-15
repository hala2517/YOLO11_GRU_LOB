from app.db.base import Base
from app.models.timestamp import TimestampMixin
from sqlalchemy import Boolean, Index, String, Text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession


class Role(TimestampMixin, Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    user_roles: Mapped[list["UserRole"]] = relationship(
        "UserRole", back_populates="role", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("ix_roles_name", "name"),)


async def seed_roles(session: AsyncSession) -> None:
    """Seed default roles if they don't exist."""
    default_roles = [
        {"name": "admin", "description": "시스템 관리자"},
        {"name": "operator", "description": "현장 운영자"},
        {"name": "viewer", "description": "모니터링 담당자"},
    ]

    for role_data in default_roles:
        result = await session.execute(
            select(Role).where(Role.name == role_data["name"])
        )
        if result.scalar_one_or_none() is None:
            session.add(Role(**role_data))

    await session.commit()


from app.models.user_role import UserRole  # noqa: E402
