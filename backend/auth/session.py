from datetime import timedelta
from typing import Union, List, Dict

from backend.auth.auth import Auth
from backend.auth.repository import UserRepository
from backend.auth.schemas import UserRead, UserCreate, UserCreateResponse, \
    UserList, UserUpdate, UserLogin
from backend.auth.utils import HashingPassword
from backend.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES


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

    async def update_user(
            self, user_id: int, params: dict) -> Union[UserUpdate, None]:
        async with self.session.begin():
            user = await self.user_rep.update_user(user_id=user_id, **params)
            if user:
                return UserUpdate(
                    username=user.username,
                    phone=user.phone,
                    email=user.email
                )

    async def auth_user(
            self, phone, password) -> Union[UserLogin, None]:
        user = await self.user_rep.get_user_by_phone(phone)
        if user:
            check_password = HashingPassword.verify_password(
                password, user[0].hashed_password)
            if check_password:
                access_token_expires = timedelta(
                    minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = Auth().create_access_token(
                    data={'some': 'payload', 'sub': f'{user[0].phone}',
                          'other_custom_data': [1, 2, 3, 4]},
                    expires_delta=access_token_expires,
                )
                return UserLogin(
                    id=user[0].id,
                    email=user[0].email,
                    username=user[0].username,
                    phone=user[0].phone,
                    is_active=user[0].is_active,
                    is_superuser=user[0].is_superuser,
                    is_verified=user[0].is_verified,
                    created=user[0].created,
                    updated=user[0].updated,
                    access_token=access_token,
                    token_type='Bearer',
                    profile={
                        'id': user[1].id,
                        'first_name': user[1].first_name,
                        'last_name': user[1].last_name,
                    }
                )
