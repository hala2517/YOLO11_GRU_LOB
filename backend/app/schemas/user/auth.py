from datetime import datetime

from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    login_id: str = Field(min_length=4, max_length=50)
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: datetime
