from pydantic import BaseModel, Field


class ProcessUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    description: str | None = None
    line_order: int | None = Field(default=None, ge=0)
    is_active: bool | None = None
