from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.auth.schemas import UserRead, UserCreate, UserCreateResponse, \
    UserList, UserDelete
from backend.auth.session import UserSession
from backend.core.session import get_async_session

user_router = APIRouter()


@user_router.get('/list', response_model=List[UserList])
async def get_users(
        session: AsyncSession = Depends(
            get_async_session)) -> List[Dict[str, UserList]]:
    users = await UserSession(session).get_users()
    return users


@user_router.get('/', response_model=UserRead)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)) -> UserRead:
    user = await UserSession(session).get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found."
        )
    return user


@user_router.post('/', response_model=UserCreateResponse)
async def create_user(
        body: UserCreate,
        session: AsyncSession = Depends(
            get_async_session)) -> UserCreateResponse:
    return await UserSession(session).create_user(body)


@user_router.delete('/delete/{user_id}', response_model=UserDelete)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)) -> UserDelete:
    delete_user_id = await UserSession(session).delete_user(user_id)
    if delete_user_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {user_id} not found')
    return UserDelete(deleted_user_id=delete_user_id)
