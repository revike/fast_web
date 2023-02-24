from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.note.models import Note


class NoteRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_notes_list(self) -> List[Note]:
        query = select(Note).filter_by(is_active=True)
        result = await self.db_session.execute(query)
        note = result.all()
        return note

    async def create_note(self, text) -> Note:
        new_note = Note(text=text)
        self.db_session.add(new_note)
        await self.db_session.flush()
        return new_note
