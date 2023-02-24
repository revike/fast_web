from typing import List, Dict

from backend.note.repository import NoteRepository
from backend.note.schemas import NoteList, NoteCreate, NoteCreateResponse


class NoteSession:

    def __init__(self, session):
        self.session = session
        self.note_rep = NoteRepository(self.session)

    async def get_notes(self) -> List[Dict[str, NoteList]]:
        async with self.session as session:
            async with session.begin():
                notes = await self.note_rep.get_notes_list()
                return [{
                    'id': note[0].id,
                    'text': note[0].text,
                    'is_active': note[0].is_active,
                    'created': note[0].created,
                    'updated': note[0].updated,
                } for note in notes]

    async def create_note(self, body: NoteCreate) -> NoteCreateResponse:
        async with self.session.begin():
            note = await self.note_rep.create_note(
                text=body.text
            )
            return NoteCreateResponse(
                id=note.id,
                text=note.text,
                is_active=note.is_active,
                created=note.created,
                updated=note.updated,
            )
