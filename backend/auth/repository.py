from typing import Union, List

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.auth.models import User, Profile


class UserRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, email: str, phone: int,
                          hashed_password: str) -> User:
        new_user = User(email=email, phone=phone, username=f'{phone}',
                        hashed_password=hashed_password)
        self.db_session.add(new_user)
        try:
            await self.db_session.flush()
            profile = Profile(user=new_user.id)
            self.db_session.add(profile)
            await self.db_session.flush()
            return new_user
        except IntegrityError as err:
            error = f'{err.__context__}'.replace('user.username', 'user.phone')
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=error)

    async def delete_user(self, user_id) -> Union[int | None]:
        query = select(User).filter_by(id=user_id, is_active=True)
        res = await self.db_session.execute(query)
        user = res.fetchone()
        if user:
            query_update = update(User).filter_by(
                id=user_id, is_active=True).values(is_active=False)
            await self.db_session.execute(query_update)
            return user_id

    async def get_users_list(self) -> List[User]:
        query = select(User).filter_by()
        res = await self.db_session.execute(query)
        user = res.all()
        return user

    async def get_user_by_id(self, user_id: int) -> Union[User | None]:
        query = select(User).filter_by(id=user_id)
        res = await self.db_session.execute(query)
        user = res.fetchone()
        if user:
            return user[0]

    async def get_profile(self, user_id: int) -> Union[User | None]:
        query = select(Profile).filter_by(user=user_id)
        res = await self.db_session.execute(query)
        profile = res.fetchone()
        if profile:
            return profile[0]

    async def get_user_by_phone(self) -> Union[User | None]:
        ...

    async def get_user_by_email(self) -> Union[User | None]:
        ...

    async def update_user(self) -> Union[int | None]:
        ...
