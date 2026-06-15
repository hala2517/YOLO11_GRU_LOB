from pydantic import BaseModel, ConfigDict, EmailStr


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr | None = None
    name: str | None = None
    is_active: bool | None = None
    password: str | None = None
