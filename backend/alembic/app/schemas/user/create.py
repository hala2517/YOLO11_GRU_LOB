from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    login_id: str = Field(min_length=4, max_length=50)
    password: str
    name: str
