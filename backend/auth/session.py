from typing import Union

from backend.auth.repository import UserRepository
from backend.auth.schemas import UserRead, UserCreate, UserCreateResponse
from backend.auth.utils import HashingPassword


class UserSession:
    def __init__(self, session):
        self.session = session

    async def get_user(self, user_id) -> Union[UserRead, None]:
        async with self.session as session:
            async with session.begin():
                user_rep = UserRepository(session)
                user = await user_rep.get_user_by_id(user_id)
                profile = await user_rep.get_profile(user_id)
                if profile is not None:
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
            user_rep = UserRepository(self.session)
            user = await user_rep.create_user(
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
