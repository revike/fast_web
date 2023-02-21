from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.session import get_async_session
from backend.note.session import NoteSession

main_router = APIRouter()


@main_router.get('/')
async def list_notes(
        session: AsyncSession = Depends(get_async_session)) -> List:
    notes = await NoteSession(session).get_notes()
    return []
