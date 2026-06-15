from pydantic import BaseModel, Field


class ProcessCreate(BaseModel):
    site_id: int
    name: str
    code: str | None = None
    description: str | None = None
    line_order: int = Field(default=0, ge=0)
    created_by: int | None = None
    is_active: bool = True
