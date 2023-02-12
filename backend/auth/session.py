from typing import Union, List, Dict

from backend.auth.repository import UserRepository
from backend.auth.schemas import UserRead, UserCreate, UserCreateResponse, \
    UserList
from backend.auth.utils import HashingPassword


class UserSession:
    def __init__(self, session):
        self.session = session
        self.user_rep = UserRepository(self.session)

    async def get_users(self) -> List[Dict[str, UserList]]:
        async with self.session as session:
            async with session.begin():
                users = await self.user_rep.get_users_list()
                return [{
                    'id': user[0].id,
                    'email': user[0].email,
                    'username': user[0].username,
                    'phone': user[0].phone,
                    'created': user[0].created,
                    'updated': user[0].updated,
                    'is_active': user[0].is_active
                } for user in users]

    async def get_user(self, user_id) -> Union[UserRead, None]:
        async with self.session as session:
            async with session.begin():
                user = await self.user_rep.get_user_by_id(user_id)
                profile = await self.user_rep.get_profile(user_id)
                if user is not None:
                    return UserRead(
                        id=user.id,
                        email=user.email,
                        username=user.username,
                        phone=user.phone,
                        is_active=user.is_active,
                        is_superuser=user.is_superuser,
                        is_verified=user.is_verified,
                        created=user.created,
                        updated=user.updated,
                        profile={
                            'id': profile.id,
                            'first_name': profile.first_name,
                            'last_name': profile.last_name,
                        }
                    )

    async def create_user(self, body: UserCreate) -> UserCreateResponse:
        async with self.session.begin():
            user = await self.user_rep.create_user(
                email=body.email,
                phone=body.phone,
                hashed_password=HashingPassword.get_password_hash(
                    body.password),
            )
            return UserCreateResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                phone=user.phone,
                created=user.created,
            )

    async def delete_user(self, user_id) -> Union[int, None]:
        async with self.session.begin():
            delete_user_id = await self.user_rep.delete_user(user_id)
            return delete_user_id
