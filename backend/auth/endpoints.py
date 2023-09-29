from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.auth.auth import OAuth2PasswordRequestBody
from backend.auth.schemas import UserRead, UserCreate, UserCreateResponse, \
    UserList, UserDelete, UserUpdate, UserLogin
from backend.auth.session import UserSession, Auth
from backend.core.session import get_async_session

user_router = APIRouter()


@user_router.get('/', response_model=List[UserList])
async def get_users(
        session: AsyncSession = Depends(get_async_session),
        token: str = Depends(Auth.decode_token)
) -> List[Dict[str, UserList]]:
    if token:
        users = await UserSession(session).get_users()
        return users


@user_router.get('/{user_id}', response_model=UserRead)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
        token: str = Depends(Auth.decode_token)) -> UserRead:
    if token:
        user = await UserSession(session).get_user(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found."
            )
        return user


@user_router.post('/register', response_model=UserCreateResponse)
async def create_user(
        body: UserCreate,
        session: AsyncSession = Depends(
            get_async_session)) -> UserCreateResponse:
    return await UserSession(session).create_user(body)


@user_router.delete('/delete/{user_id}', response_model=UserDelete)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
        token: str = Depends(Auth.decode_token)) -> UserDelete:
    if token:
        delete_user_id = await UserSession(session).delete_user(user_id)
        if delete_user_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'User with id {user_id} not found')
        return UserDelete(deleted_user_id=delete_user_id)


@user_router.patch('/update/{user_id}', response_model=UserUpdate)
async def update_user(
        user_id: int,
        body: UserUpdate,
        session: AsyncSession = Depends(get_async_session),
        token: str = Depends(Auth.decode_token)) -> UserUpdate:
    if token:
        updated_user_params = body.dict(exclude_none=True)
        if updated_user_params == {}:
            raise HTTPException(
                status_code=422,
                detail='You must specify at least one user update option',
            )
        user = await UserSession(session).update_user(
            user_id, updated_user_params)
        if user is None:
            raise HTTPException(
                status_code=404, detail=f"User with id {user_id} not found."
            )

        return UserUpdate(
            username=user.username,
            phone=user.phone,
            email=user.email
        )


@user_router.post("/login", response_model=UserLogin)
async def login_for_access_token(
        data: OAuth2PasswordRequestBody = Depends(),
        session: AsyncSession = Depends(get_async_session)) -> UserLogin:
    user = await UserSession(session).auth_user(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone or password",
        )
    return user
