from pydantic import BaseModel


class DatasetCreate(BaseModel):
    name: str
    description: str | None = None
    total_images: int = 0
    labeled_images: int = 0
    storage_path: str | None = None
    version: str | None = None
    is_active: bool = True
    created_by: int | None = None
