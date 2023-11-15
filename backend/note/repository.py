from typing import List

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
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

    async def get_note_by_id(self, note_id) -> Note | None:
        query = select(Note).filter_by(id=note_id, is_active=True)
        res = await self.db_session.execute(query)
        note = res.fetchone()
        if note:
            return note[0]

    async def update_note(self, note_id, **kwargs) -> Note | None:
        query = select(Note).filter_by(id=note_id, is_active=True)
        res = await self.db_session.execute(query)
        note = res.fetchone()
        if note:
            try:
                query_update = update(Note).filter_by(id=note_id, is_active=True).values(kwargs)
                await self.db_session.execute(query_update)
                return note[0]
            except IntegrityError as err:
                raise HTTPException(status_code=503, detail=f'{err.__context__}')
