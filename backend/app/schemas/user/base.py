from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    login_id: str
    email: EmailStr | None = None
    name: str
    is_active: bool = True
