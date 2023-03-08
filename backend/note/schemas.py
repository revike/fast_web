from datetime import datetime

from pydantic import BaseModel


class NoteList(BaseModel):
    id: int
    text: str
    is_active: bool
    created: datetime
    updated: datetime


class NoteCreate(BaseModel):
    text: str


class NoteCreateResponse(BaseModel):
    id: int
    text: str
    is_active: bool
    created: datetime
    updated: datetime


class NoteItem(BaseModel):
    id: int
    text: str
    is_active: bool
    created: datetime
    updated: datetime


class NoteUpdate(BaseModel):
    text: str
