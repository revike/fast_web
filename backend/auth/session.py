from typing import Union

from backend.auth.repository import UserRepository
from backend.auth.schemas import UserRead, UserCreate
from backend.auth.utils import HashingPassword


class UserSession:
    def __init__(self, session):
        self.session = session

    async def get_user(self, user_id) -> Union[UserRead, None]:
        async with self.session as session:
            async with session.begin():
                user_rep = UserRepository(session)
                profile = await user_rep.get_profile(user_id)
                if profile is not None:
                    return UserRead(
                        id=profile.user_.id,
                        email=profile.user_.email,
                        username=profile.user_.username,
                        phone=profile.user_.phone,
                        is_active=profile.user_.is_active,
                        is_superuser=profile.user_.is_superuser,
                        is_verified=profile.user_.is_verified,
                        created=profile.user_.created,
                        updated=profile.user_.updated,
                        profile={
                            'id': profile.id,
                            'first_name': profile.first_name,
                            'last_name': profile.last_name,
                        }
                    )

    async def create_user(self, body: UserCreate) -> UserRead:
        async with self.session.begin():
            user_rep = UserRepository(self.session)
            user = await user_rep.create_user(
                email=body.email,
                phone=body.phone,
                hashed_password=HashingPassword.get_password_hash(
                    body.password),
            )
            return UserRead(
                id=user.id,
                email=user.email,
                username=user.username,
                phone=user.phone,
                created=user.created,
                updated=user.updated,
            )
