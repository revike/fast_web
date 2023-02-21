from datetime import datetime

from pydantic import BaseModel


class NoteList(BaseModel):
    id: int
    text: str
    is_active: bool
    created: datetime
    updated: datetime
