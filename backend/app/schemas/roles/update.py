from pydantic import BaseModel


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
