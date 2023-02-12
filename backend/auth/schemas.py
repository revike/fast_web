from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr

from backend.auth.validators import DefaultModel


class UserList(BaseModel):
    id: int
    email: EmailStr
    username: str
    phone: int
    created: datetime
    updated: datetime
    is_active: bool


class ProfileRead(BaseModel):
    id: int
    first_name: Optional[str | None]
    last_name: Optional[str | None]

    class Config:
        orm_mode = True


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    phone: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    created: datetime
    updated: datetime
    profile: ProfileRead

    class Config:
        orm_mode = True


class UserLogin(UserRead):
    access_token: str
    token_type: str


class UserCreate(DefaultModel):
    email: EmailStr
    phone: int
    password: str


class UserCreateResponse(DefaultModel):
    id: int
    email: EmailStr
    username: str
    phone: int
    created: datetime


class UserDelete(BaseModel):
    deleted_user_id: int


class UserUpdate(DefaultModel):
    username: Optional[constr(min_length=1)]
    phone: int
    email: Optional[EmailStr]
