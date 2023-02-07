from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, constr, validator

from backend.auth.validators import validate_user_phone


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


class UserCreate(BaseModel):
    email: EmailStr
    phone: int
    password: str

    @validator('phone')
    def validate_phone(cls, value):
        if not validate_user_phone(value):
            raise HTTPException(
                status_code=422, detail='Phone entered incorrectly')
        return value


class UserDeleteResponse(BaseModel):
    deleted_user_id: int


class UserUpdatedResponse(BaseModel):
    updated_user_id: int


class UserUpdateRequest(BaseModel):
    username: Optional[constr(min_length=1)]
    phone: int
    email: Optional[EmailStr]
