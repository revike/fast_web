import re

from fastapi import HTTPException
from pydantic import BaseModel, validator


class DefaultModel(BaseModel):
    @staticmethod
    def validate_user_phone(value):
        """Валидация phone"""
        pattern = r'^\d{10}$'
        if re.match(pattern, str(value)):
            return value

    @validator('phone', check_fields=False)
    def validate_phone(cls, value):
        if not cls.validate_user_phone(value):
            raise HTTPException(
                status_code=422, detail='Phone entered incorrectly')
        return value
