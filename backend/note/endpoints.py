from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.auth import Auth
from backend.core.session import get_async_session
from backend.note.schemas import NoteList, NoteCreate, NoteCreateResponse
from backend.note.session import NoteSession

note_router = APIRouter()


@note_router.get('/', response_model=List[NoteList])
async def list_notes(
        session: AsyncSession = Depends(get_async_session),
        token: str = Depends(Auth.decode_token)
) -> List:
    if token:
        notes = await NoteSession(session).get_notes()
        return notes


@note_router.post('/create', response_model=NoteCreateResponse)
async def create_note(
        body: NoteCreate,
        session: AsyncSession = Depends(get_async_session),
        token: str = Depends(Auth.decode_token)
) -> NoteCreateResponse:
    if token:
        return await NoteSession(session).create_note(body)
