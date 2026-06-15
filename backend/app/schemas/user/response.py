from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    """기본 사용자 응답 — roles 미포함 (현재 기본값)"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    login_id: str
    name: str
    email: str | None = None
    created_at: datetime
    updated_at: datetime


class UserWithRolesResponse(UserResponse):
    """roles 정보 포함 응답 — 필요한 엔드포인트에서만 명시적으로 사용"""

    roles: List[str] = []

    @classmethod
    def from_orm_with_roles(cls, user: object) -> "UserWithRolesResponse":
        role_names = [r.name for r in getattr(user, "roles", [])]
        base = cls.model_validate(user)
        base.roles = role_names
        return base
