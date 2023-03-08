from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.auth.auth import Auth
from backend.core.session import get_async_session
from backend.note.schemas import NoteList, NoteCreate, NoteCreateResponse, NoteItem, NoteUpdate
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


@note_router.get('/{note_id}', response_model=NoteItem)
async def note_item(
        note_id: int, session: AsyncSession = Depends(get_async_session),
        token: str = Depends(Auth.decode_token)) -> NoteItem:
    if token:
        note = await NoteSession(session).get_note(note_id)
        if note is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {note_id} not found."
            )
        return note


@note_router.patch('/update/{note_id}', response_model=NoteItem)
async def note_update(
        note_id: int,
        body: NoteUpdate,
        session: AsyncSession = Depends(get_async_session),
        token: str = Depends(Auth.decode_token)) -> NoteUpdate:
    if token:
        updated_note_params = body.dict(exclude_none=True)
        if updated_note_params == {}:
            raise HTTPException(
                status_code=422,
                detail='You must specify at least one note update option',
            )
        note = await NoteSession(session).update_note(
            note_id, updated_note_params)
        if note is None:
            raise HTTPException(
                status_code=404, detail=f"User with id {note_id} not found."
            )

        return NoteUpdate(
            username=note.text
        )
